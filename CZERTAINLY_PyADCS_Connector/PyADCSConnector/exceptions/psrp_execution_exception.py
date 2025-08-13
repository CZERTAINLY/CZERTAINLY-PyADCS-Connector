class PsrpExecutionException(Exception):
    """
    Exception raised when a PowerShell Remoting Protocol (PSRP) command execution fails.
    This exception contains the status code and standard error output from the failed command.
    """
    def __init__(self, status_code, std_err):
        self.status_code = status_code
        self.std_err = std_err
