from enum import Enum


class RemotingProtocol(Enum):
    WINRM = "WinRM"
    PSRP = "PSRP"
