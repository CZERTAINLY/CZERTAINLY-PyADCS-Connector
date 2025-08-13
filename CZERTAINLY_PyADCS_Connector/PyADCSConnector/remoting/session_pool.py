import threading
import time
import logging
from collections import deque
from typing import Callable, Deque, Optional, Tuple

from .session_adapters import SessionAdapter

logger = logging.getLogger(__name__)

class SessionPool:
    """
    Thread-safe pool for SessionAdapter instances.
    """
    def __init__(
        self,
        factory: Callable[[], SessionAdapter],
        *,
        maxsize: int = 10,
        min_warm: int = 1,
        keepalive_interval_s: int = 25,   # ping often enough to avoid idle timeouts
        acquire_timeout_s: Optional[float] = None,
        max_idle_s: Optional[int] = 600,  # trim idle > 10m (None = never)
        name: str = "session-pool",
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

        self._lock = threading.Lock()
        self._cv = threading.Condition(self._lock)
        self._idle: Deque[Tuple[SessionAdapter, float]] = deque()  # (session, last_used_ts)
        self._in_use = 0
        self._total = 0
        self._closed = False

        # warm up (lazy: optionally create min_warm synchronously)
        for _ in range(self._min_warm):
            self._idle.append((self._create_connected(), time.time()))

        # start keepalive/maintenance thread
        self._bg = threading.Thread(target=self._maintainer, name=f"{self._name}-keeper", daemon=True)
        self._bg.start()

    # ---------- public API ----------

    def acquire(self, timeout: Optional[float] = None) -> SessionAdapter:
        """
        Block until a session is available; create new if under maxsize.
        Returns a live, healthy session.
        """
        deadline = time.time() + (timeout if timeout is not None else (self._acquire_timeout_s or 1e12))
        with self._cv:
            while True:
                if self._closed:
                    raise RuntimeError("Pool is closed")

                # Reuse idle session if any
                if self._idle:
                    s, _ = self._idle.popleft()
                    self._in_use += 1
                    # sanity check: ensure healthy
                    if not self._safe_ping(s):
                        self._destroy(s)
                        self._in_use -= 1
                        continue  # try again in the loop
                    return s

                # Create a new one if allowed
                if self._total < self._maxsize:
                    self._in_use += 1
                    s = self._create_connected()
                    return s

                # Else wait until someone releases
                remaining = deadline - time.time()
                if remaining <= 0:
                    raise TimeoutError("Timed out acquiring a session from the pool")

                self._cv.wait(timeout=remaining)

    def release(self, session: SessionAdapter) -> None:
        """
        Return a session to the pool. If unhealthy, it is destroyed and a waiter is notified.
        """
        with self._cv:
            if self._closed:
                # if closed, we just destroy it
                self._destroy(session)
                return

            if not self._safe_ping(session):
                self._destroy(session)
                self._in_use -= 1
                self._cv.notify()
                return

            self._idle.append((session, time.time()))
            self._in_use -= 1
            self._cv.notify()  # wake one waiter

    def close(self) -> None:
        """
        Close the pool and all held sessions.
        """
        with self._cv:
            self._closed = True
            # destroy all idle
            while self._idle:
                s, _ = self._idle.popleft()
                self._destroy(s)
            # Note: sessions currently in use will be destroyed when released
            self._cv.notify_all()

    # ---------- context helper ----------

    def borrow(self, timeout: Optional[float] = None):
        """
        Context manager:  with pool.borrow() as s: s.run_ps(...)
        """
        pool = self
        class _BorrowCtx:
            def __enter__(self_inner):
                self_inner._sess = pool.acquire(timeout)
                return self_inner._sess
            def __exit__(self_inner, exc_type, exc, tb):
                pool.release(self_inner._sess)
                return False
        return _BorrowCtx()

    # ---------- internals ----------

    def _create_connected(self) -> SessionAdapter:
        s = self._factory()
        try:
            s.connect()
        except Exception:
            logger.exception("Failed to connect new session")
            # If connect fails, do not increase totals
            raise
        self._total += 1
        return s

    def _destroy(self, s: SessionAdapter) -> None:
        try:
            s.disconnect()
        except Exception:
            logger.debug("Ignoring error on disconnect", exc_info=True)
        self._total -= 1

    def _safe_ping(self, s: SessionAdapter) -> bool:
        try:
            return s.ping()
        except Exception:
            return False

    def _maintainer(self):
        interval = max(5, self._keepalive_interval_s)
        while True:
            time.sleep(interval)
            with self._cv:
                if self._closed:
                    return

                # Keepalive: ping idle sessions; repair/replace if needed
                now = time.time()
                new_idle: Deque[Tuple[SessionAdapter, float]] = deque()
                unhealthy = 0
                trimmed = 0

                # Trim excess idle (respect min_warm)
                target_keep = max(self._min_warm, 0)
                # First pass: ping and keep healthy
                while self._idle:
                    s, last_used = self._idle.popleft()

                    # Optional idle trimming
                    if self._max_idle_s is not None and (now - last_used) > self._max_idle_s and self._total > target_keep:
                        self._destroy(s)
                        trimmed += 1
                        continue

                    if not self._safe_ping(s):
                        self._destroy(s)
                        unhealthy += 1
                        continue

                    new_idle.append((s, last_used))

                self._idle = new_idle

                # If we fell below the warm baseline, top up
                while (self._total < self._maxsize) and (len(self._idle) + self._in_use < target_keep):
                    try:
                        self._idle.append((self._create_connected(), now))
                    except Exception:
                        break  # avoid tight loop if remote is down

                if unhealthy or trimmed:
                    logger.debug("[%s] maintainer: unhealthy=%s trimmed=%s total=%s in_use=%s idle=%s",
                                 self._name, unhealthy, trimmed, self._total, self._in_use, len(self._idle))
