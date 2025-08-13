import logging
from base64 import b64encode

from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.remoting.psrp_remoting import create_psrp_session_from_authority_instance
from PyADCSConnector.remoting.remote_result import RemoteResult
from PyADCSConnector.remoting.remoting_protocol import RemotingProtocol
from PyADCSConnector.remoting.winrm_remoting import create_winrm_session_from_authority_instance

logger = logging.getLogger(__name__)


def winrm_limit_reached(script: str) -> bool:
    """
    Check if the script length exceeds the WinRM limit of 8192 characters.
    """
    length = len(b64encode(script.encode('utf_16_le')))
    return length > 8192


def invoke_remote_script_uuid(authority_instance_uuid: str, script: str) -> RemoteResult:
    authority_instance = AuthorityInstance.objects.get(uuid=authority_instance_uuid)
    return invoke_remote_script(authority_instance, script)


def invoke_remote_script(authority_instance: AuthorityInstance, script: str) -> RemoteResult:
    remoting_protocol = RemotingProtocol.WINRM
    if winrm_limit_reached(script):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Script length exceeds WinRM limit, switching to PSRP remoting.")
        remoting_protocol = RemotingProtocol.PSRP

    if remoting_protocol == RemotingProtocol.WINRM:
        session = create_winrm_session_from_authority_instance(authority_instance)
    elif remoting_protocol == RemotingProtocol.PSRP:
        session = create_psrp_session_from_authority_instance(authority_instance)

    session.connect()
    result = session.run_ps(script)
    session.disconnect()
    return result
