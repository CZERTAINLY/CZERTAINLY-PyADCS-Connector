import threading
import time
import logging
from collections import deque
from typing import Callable, Deque, Optional, Tuple

from .session_adapters import SessionAdapter

logger = logging.getLogger(__name__)

class SessionPool:
    def __init__(
        self,
        factory: Callable[[], SessionAdapter],
        *,
        maxsize: int = 10,
        min_warm: int = 1,              # how many we'd like to keep hot
        keepalive_interval_s: int = 120,
        acquire_timeout_s: Optional[float] = None,
        max_idle_s: Optional[int] = 900,
        name: str = "session-pool",

        # NEW: background warm-up controls
        eager_warm: bool = False,       # if True, start warmer immediately; else on first acquire
        warm_target: Optional[int] = None,  # default = min_warm
        warm_parallelism: int = 2,      # build at most N sessions concurrently
    ):
        if maxsize < 1:
            raise ValueError("maxsize must be >= 1")
        if min_warm < 0 or min_warm > maxsize:
            raise ValueError("min_warm must be in [0, maxsize]")

        self._factory = factory
        self._maxsize = maxsize
        self._min_warm = min_warm
        self._keepalive_interval_s = keepalive_interval_s
        self._acquire_timeout_s = acquire_timeout_s
        self._max_idle_s = max_idle_s
        self._name = name

        self._warm_target = warm_target if warm_target is not None else min_warm
        self._warm_parallelism = max(1, warm_parallelism)

        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)
        self._idle: Deque[Tuple[SessionAdapter, float]] = deque()
        self._in_use = 0
        self._total = 0
        self._closed = False

        # NEW
        self._warmer_started = False

        # maintainer keeps sessions healthy/trimmed
        self._bg = threading.Thread(target=self._maintainer, name=f"{self._name}-keeper", daemon=True)
        self._bg.start()

        if eager_warm:
            self._start_warmer()

    # ---------- public API ----------

    def acquire(self, timeout: Optional[float] = None) -> SessionAdapter:
        deadline = time.time() + (timeout if timeout is not None else (self._acquire_timeout_s or 1e12))
        with self._cv:
            # ensure warmer is running (first request)
            self._start_warmer()

            while True:
                if self._closed:
                    raise RuntimeError("Pool is closed")

                if self._idle:
                    s, _ = self._idle.popleft()
                    self._in_use += 1
                    return s

                if self._total < self._maxsize:
                    # Create exactly ONE session for this caller and return it immediately.
                    self._in_use += 1
                    s = self._create_connected_unlocked()
                    return s

                remaining = deadline - time.time()
                if remaining <= 0:
                    raise TimeoutError("Timed out acquiring a session from the pool")
                self._cv.wait(timeout=remaining)

    def release(self, session: SessionAdapter) -> None:
        with self._cv:
            if self._closed:
                self._destroy_unlocked(session)
                return
            self._idle.append((session, time.time()))
            self._in_use -= 1
            self._cv.notify()

    def close(self) -> None:
        with self._cv:
            self._closed = True
            while self._idle:
                s, _ = self._idle.popleft()
                self._destroy_unlocked(s)
            self._cv.notify_all()

    def borrow(self, timeout: Optional[float] = None):
        pool = self
        class _Borrow:
            def __enter__(self_inner):
                self_inner._s = pool.acquire(timeout)
                return self_inner._s
            def __exit__(self_inner, exc_t, exc, tb):
                pool.release(self_inner._s)
                return False
        return _Borrow()

    # ---------- internals ----------

    def _create_connected_unlocked(self) -> SessionAdapter:
        # lock is already held by caller
        s = self._factory()
        try:
            s.connect()
            # Optional one-time init if your adapter implements it
            if hasattr(s, "init"):
                try:
                    s.init()
                except Exception:
                    logger.debug("session init failed; continuing", exc_info=True)
        except Exception:
            logger.exception("Failed to connect new session")
            raise
        self._total += 1
        return s

    def _destroy_unlocked(self, s: SessionAdapter) -> None:
        try: s.disconnect()
        except Exception: logger.debug("Ignoring error on disconnect", exc_info=True)
        self._total -= 1

    def _start_warmer(self):
        if self._warmer_started:
            return
        self._warmer_started = True
        t = threading.Thread(target=self._warmer, name=f"{self._name}-warmer", daemon=True)
        t.start()

    def _warmer(self):
        """
        Build up to warm_target sessions in the background without blocking callers.
        Respects maxsize and in_use counts.
        """
        backoff = 0.05
        while True:
            with self._cv:
                if self._closed:
                    return
                target = max(0, min(self._warm_target, self._maxsize))

                # How many sessions exist or are in-use
                have = self._total
                want = max(0, target - have)

                # also ensure we don't exceed maxsize when callers are in-use
                room = max(0, self._maxsize - self._total)
                to_create = min(want, room, self._warm_parallelism)

                if to_create == 0:
                    # Re-check later; don't spin
                    pass
                else:
                    # create N sessions while briefly releasing the lock per session
                    for _ in range(to_create):
                        if self._closed:
                            return
                        # Create one
                        try:
                            s = self._factory()
                            # Release lock while connecting (slow I/O), reacquire to update counters
                            self._cv.release()
                            try:
                                s.connect()
                                if hasattr(s, "init"):
                                    try:
                                        s.init()
                                    except Exception:
                                        logger.debug("session init failed; continuing", exc_info=True)
                            except Exception:
                                logger.exception("warmer failed to connect session")
                                # drop and continue; small backoff
                                try:
                                    s.disconnect()
                                except Exception:
                                    pass
                                time.sleep(0.2)
                            finally:
                                self._cv.acquire()

                            # If pool closed during connect, discard
                            if self._closed:
                                try: s.disconnect()
                                except Exception: pass
                                return

                            self._idle.append((s, time.time()))
                            self._total += 1
                            self._cv.notify()
                        except Exception:
                            logger.exception("warmer factory failure")
                            time.sleep(0.2)

            # sleep a bit before next pass; increase if we failed repeatedly
            time.sleep(backoff)
            backoff = min(backoff * 2, 1.0)

    def _maintainer(self):
        interval = max(5, self._keepalive_interval_s)
        while True:
            time.sleep(interval)
            with self._cv:
                if self._closed:
                    return
                now = time.time()
                new_idle: Deque[Tuple[SessionAdapter, float]] = deque()
                unhealthy = 0
                trimmed = 0
                target_keep = max(self._min_warm, 0)

                while self._idle:
                    s, last_used = self._idle.popleft()
                    if self._max_idle_s is not None and (now - last_used) > self._max_idle_s and self._total > target_keep:
                        self._destroy_unlocked(s); trimmed += 1; continue
                    # cheap health check only here (not on acquire)
                    try:
                        ok = s.ping()
                    except Exception:
                        ok = False
                    if not ok:
                        self._destroy_unlocked(s); unhealthy += 1; continue
                    new_idle.append((s, last_used))

                self._idle = new_idle

                # top-up to min_warm if needed (1-by-1, non-blocking)
                while (self._total < self._maxsize) and (len(self._idle) + self._in_use < target_keep):
                    try:
                        s = self._factory()
                        self._cv.release()
                        try:
                            s.connect()
                            if hasattr(s, "init"):
                                try:
                                    s.init()
                                except Exception:
                                    logger.debug("session init failed; continuing", exc_info=True)
                        finally:
                            self._cv.acquire()
                        self._idle.append((s, now))
                        self._total += 1
                    except Exception:
                        break

                if unhealthy or trimmed:
                    logger.debug("[%s] maintainer: unhealthy=%s trimmed=%s total=%s in_use=%s idle=%s",
                                 self._name, unhealthy, trimmed, self._total, self._in_use, len(self._idle))
