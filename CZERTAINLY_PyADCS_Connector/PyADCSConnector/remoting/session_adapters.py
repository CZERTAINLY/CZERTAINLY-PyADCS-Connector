import logging
from typing import Protocol

logger = logging.getLogger(__name__)

class SessionAdapter(Protocol):
    def connect(self) -> None: ...
    def disconnect(self) -> None: ...
    def run_ps(self, script: str): ...
    def ping(self) -> bool: ...

class WinRMAdapter:
    def __init__(self, inner, key):  # inner = WinRmRemoting
        self._s = inner
        self.key = key

    def init(self) -> None:
        # One-time run when the session is created.
        init_script = r"""
            $ProgressPreference = 'SilentlyContinue'
            $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
        """
        self.run_ps(init_script)

    def connect(self): self._s.connect()
    def disconnect(self): self._s.disconnect()
    def run_ps(self, script: str): return self._s.run_ps(script)

    def ping(self) -> bool:
        try:
            # cheap, low-output no-op
            logger.debug(f"Pinging {self.key}")
            return self._s.run_ps("$null=1").status_code == 0
        except Exception:
            logger.exception("WinRM keepalive ping failed")
            return False


class PSRPAdapter:
    def __init__(self, inner, key):  # inner = PsrpRemoting
        self._s = inner
        self.key = key

    def init(self) -> None:
        # One-time run when the session is created.
        init_script = r"""
            $ProgressPreference = 'SilentlyContinue'
            $PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'
        """
        self.run_ps(init_script)

    def connect(self): self._s.connect()
    def disconnect(self): self._s.disconnect()
    def run_ps(self, script: str): return self._s.run_ps(script)

    def ping(self) -> bool:
        try:
            logger.debug(f"Pinging {self.key}")
            res = self._s.run_ps("$null=1")
            return res.status_code == 0 and not res.had_errors
        except Exception:
            logger.exception("PSRP keepalive ping failed")
            return False
