import logging
from typing import Protocol

logger = logging.getLogger(__name__)

class SessionAdapter(Protocol):
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def run_ps(self, script: str): ...
    def ping(self) -> bool: ...

class WinRMAdapter:
    def __init__(self, inner):  # inner = WinRmRemoting
        self._s = inner

    def connect(self): self._s.connect()
    def disconnect(self): self._s.disconnect()
    def run_ps(self, script: str): return self._s.run_ps(script)

    def ping(self) -> bool:
        try:
            # cheap, low-output no-op
            # avoids large outputs and doesn’t hit WinRM’s 8192 encoded limit
            res = self._s.run_ps("$PSVersionTable.PSVersion | Out-Null")
            return res.status_code == 0
        except Exception:
            logger.exception("WinRM keepalive ping failed")
            return False


class PSRPAdapter:
    def __init__(self, inner):  # inner = PsrpRemoting
        self._s = inner

    def connect(self): self._s.connect()
    def disconnect(self): self._s.disconnect()
    def run_ps(self, script: str): return self._s.run_ps(script)

    def ping(self) -> bool:
        try:
            res = self._s.run_ps("$null = $PSVersionTable;")
            return res.status_code == 0 and not res.had_errors
        except Exception:
            logger.exception("PSRP keepalive ping failed")
            return False
