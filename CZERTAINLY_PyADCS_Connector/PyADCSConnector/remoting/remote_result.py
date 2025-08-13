from dataclasses import dataclass


@dataclass
class RemoteResult:
    """
    Represents the result of executing a remote script or command.
    Attributes:
        status_code (int): The exit status code returned by the remote process.
        std_out (bytes): The standard output produced by the remote process.
        std_err (bytes): The standard error output produced by the remote process.
        had_errors (bool): Indicates whether any errors occurred during execution.
    """
    status_code: int
    std_out: bytes
    std_err: bytes
    had_errors: bool = False
