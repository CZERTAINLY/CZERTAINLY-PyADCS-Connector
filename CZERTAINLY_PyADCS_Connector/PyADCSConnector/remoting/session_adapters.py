import logging
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Callable, Any

logger = logging.getLogger(__name__)


class InnerPSSession(Protocol):
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def run_ps(self, script: str) -> Any: ...

@runtime_checkable
class SessionAdapter(Protocol):
    key: str
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def run_ps(self, script: str) -> Any: ...
    def ping(self) -> bool: ...
    def init(self) -> None: ...  # make it part of the contract to avoid hasattr checks

SHARED_INIT_SCRIPT = r"""
    $ProgressPreference = 'SilentlyContinue'
    $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
"""

PingOk = Callable[[Any], bool]

@dataclass
class _BasePSAdapter(SessionAdapter):
    inner: InnerPSSession
    key: str
    name: str
    ping_ok: PingOk

    def init(self) -> None:
        self.run_ps(SHARED_INIT_SCRIPT)

    def connect(self) -> None: self.inner.connect()
    def disconnect(self) -> None: self.inner.disconnect()
    def run_ps(self, script: str): return self.inner.run_ps(script)

    def ping(self) -> bool:
        try:
            logger.debug(f"Pinging {self.key}")
            res = self.inner.run_ps("$null=1")
            return self.ping_ok(res)
        except Exception:
            logger.exception(f"{self.name} keepalive ping failed")
            return False


class WinRMAdapter(_BasePSAdapter):
    def __init__(self, inner: InnerPSSession, key: str):
        super().__init__(
            inner=inner,
            key=key,
            name="WinRM",
            ping_ok=lambda r: getattr(r, "status_code", 1) == 0,
        )

class PSRPAdapter(_BasePSAdapter):
    def __init__(self, inner: InnerPSSession, key: str):
        super().__init__(
            inner=inner,
            key=key,
            name="PSRP",
            ping_ok=lambda r: getattr(r, "status_code", 1) == 0 and not getattr(r, "had_errors", False),
        )
