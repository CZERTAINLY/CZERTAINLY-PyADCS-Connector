import threading
import time
import logging
from collections import deque
from typing import Callable, Deque, Optional, Tuple

from PyADCSConnector.remoting.session_adapters import SessionAdapter

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

        # background warm-up controls
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

        self._warmer_started = False

        # maintainer keeps sessions healthy/trimmed
        self._bg = threading.Thread(target=self._maintainer, name=f"{self._name}-keeper", daemon=True)
        self._bg.start()

        if eager_warm:
            self._start_warmer()

    # ---------- public API ----------

    def force_new(self) -> "SessionAdapter":
        """
        Create and return a brand new connected session without using idle pool.
        The caller is responsible for releasing it back with `release()` when done.
        """
        with self._cv:
            if self._closed:
                raise RuntimeError("Pool is closed")
            s = self._create_connected_unlocked()
            self._in_use += 1
            return s

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

    # ---------- internals (shared) ----------

    def _create_connected_unlocked(self) -> SessionAdapter:
        # lock is already held by caller
        s = self._factory()
        try:
            s.connect()
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
        try:
            s.disconnect()
        except Exception:
            logger.debug("Ignoring error on disconnect", exc_info=True)
        self._total -= 1

    def _start_warmer(self):
        if self._warmer_started:
            return
        self._warmer_started = True
        t = threading.Thread(target=self._warmer, name=f"{self._name}-warmer", daemon=True)
        t.start()

    # ---------- helpers used by _maintainer ----------

    def _health_check_unlocked(self, s: SessionAdapter) -> bool:
        """Return True if the session responds to ping(); lock must be held."""
        try:
            return s.ping()
        except Exception:
            return False

    def _should_trim_unlocked(self, now: float, last_used: float, target_keep: int) -> bool:
        """Decide whether to trim an idle session based on age and keep target."""
        if self._max_idle_s is None:
            return False
        return (now - last_used) > self._max_idle_s and self._total > target_keep

    def _connect_new_session_outside_lock(self) -> Optional[SessionAdapter]:
        """
        Create/connect/init a session while releasing the condition lock to avoid blocking.
        Returns a connected session or None on failure. Lock is held on entry and exit.
        """
        try:
            s = self._factory()
        except Exception:
            logger.debug("maintainer factory failure", exc_info=True)
            return None

        self._cv.release()
        try:
            try:
                s.connect()
                if hasattr(s, "init"):
                    try:
                        s.init()
                    except Exception:
                        logger.debug("session init failed; continuing", exc_info=True)
            except Exception:
                logger.debug("maintainer failed to connect session", exc_info=True)
                try:
                    s.disconnect()
                except Exception:
                    pass
                return None
            return s
        finally:
            self._cv.acquire()

    def _rebuild_idle_queue_unlocked(self, now: float, target_keep: int) -> Tuple[int, int]:
        """
        Sweep idle sessions: trim stale, drop unhealthy, keep good ones.
        Returns (unhealthy_count, trimmed_count). Lock must be held.
        """
        new_idle: Deque[Tuple[SessionAdapter, float]] = deque()
        unhealthy = 0
        trimmed = 0

        while self._idle:
            s, last_used = self._idle.popleft()

            if self._should_trim_unlocked(now, last_used, target_keep):
                self._destroy_unlocked(s)
                trimmed += 1
                continue

            if not self._health_check_unlocked(s):
                self._destroy_unlocked(s)
                unhealthy += 1
                continue

            new_idle.append((s, last_used))

        self._idle = new_idle
        return unhealthy, trimmed

    def _top_up_min_warm_unlocked(self, target_keep: int, now: float) -> None:
        """
        Top up the pool to at least target_keep sessions (idle+in_use),
        without exceeding maxsize. Lock must be held.
        """
        while (self._total < self._maxsize) and (len(self._idle) + self._in_use < target_keep):
            s = self._connect_new_session_outside_lock()
            if s is None:
                break  # stop on first failure; try again next tick

            if self._closed:
                try:
                    s.disconnect()
                except Exception:
                    pass
                return

            self._idle.append((s, now))
            self._total += 1

    # ---------- maintainer ----------

    def _maintainer(self):
        interval = max(5, self._keepalive_interval_s)
        while True:
            time.sleep(interval)
            with self._cv:
                if self._closed:
                    return

                now = time.time()
                target_keep = max(self._min_warm, 0)

                unhealthy, trimmed = self._rebuild_idle_queue_unlocked(now, target_keep)
                self._top_up_min_warm_unlocked(target_keep, now)

                if unhealthy or trimmed:
                    logger.debug(
                        "[%s] maintainer: unhealthy=%s trimmed=%s total=%s in_use=%s idle=%s",
                        self._name, unhealthy, trimmed, self._total, self._in_use, len(self._idle)
                    )

    # ---------- helpers used by _warmer ----------

    def _warm_batch_size_unlocked(self) -> int:
        """
        Decide how many sessions to create this tick, respecting:
        - warm target
        - maxsize
        - parallelism
        """
        target = max(0, min(self._warm_target, self._maxsize))
        have = self._total
        want = max(0, target - have)
        room = max(0, self._maxsize - self._total)
        return min(want, room, self._warm_parallelism)

    def _try_build_one_warm_session_unlocked(self) -> bool:
        """
        Build one session (releasing the lock during connect) and enqueue it as idle.
        Returns True on success, False on failure. Lock must be held on entry/exit.
        """
        try:
            s = self._factory()
        except Exception:
            logger.exception("warmer factory failure")
            return False

        self._cv.release()
        try:
            try:
                s.connect()
                if hasattr(s, "init"):
                    try:
                        s.init()
                    except Exception:
                        logger.debug("session init failed; continuing", exc_info=True)
            except Exception:
                logger.exception("warmer failed to connect session")
                try:
                    s.disconnect()
                except Exception:
                    pass
                time.sleep(0.2)  # small backoff on per-attempt failure
                return False
        finally:
            self._cv.acquire()

        if self._closed:
            try:
                s.disconnect()
            except Exception:
                pass
            return False

        self._idle.append((s, time.time()))
        self._total += 1
        self._cv.notify()
        return True

    # ---------- warmer ----------

    def _warm_tick_unlocked(self) -> bool:
        """
        One warmer tick. Returns True if the pool is closed (caller should stop).
        Lock must be held on entry/exit.
        """
        if self._closed:
            return True

        to_create = self._warm_batch_size_unlocked()

        # Loop does nothing if to_create == 0 (no extra branch needed).
        for _ in range(to_create):
            if self._closed:
                return True
            # Guard against races even though _warm_batch_size_unlocked() respects maxsize.
            if self._total >= self._maxsize:
                break
            self._try_build_one_warm_session_unlocked()

        return False

    def _warmer(self):
        """
        Build up to warm_target sessions in the background without blocking callers.
        Respects maxsize and in_use counts.
        """
        backoff = 0.05
        while True:
            with self._cv:
                if self._warm_tick_unlocked():
                    return
            time.sleep(backoff)
            backoff = min(backoff * 2, 1.0)
