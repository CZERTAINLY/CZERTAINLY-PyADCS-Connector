from dataclasses import dataclass


@dataclass
class RemoteResult:
    status_code: int
    std_out: bytes
    std_err: bytes
    had_errors: bool = False
