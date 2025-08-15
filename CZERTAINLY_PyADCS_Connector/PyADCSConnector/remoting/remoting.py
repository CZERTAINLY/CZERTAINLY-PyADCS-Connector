import logging
from base64 import b64encode

from CZERTAINLY_PyADCS_Connector.settings import ADCS_POOL_ENABLED
from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.remoting.pool_manager import global_pool_manager
from PyADCSConnector.remoting.psrp_remoting import create_psrp_session_from_authority_instance
from PyADCSConnector.remoting.remote_result import RemoteResult
from PyADCSConnector.remoting.remoting_protocol import RemotingProtocol
from PyADCSConnector.remoting.winrm_remoting import create_winrm_session_from_authority_instance

logger = logging.getLogger(__name__)

def winrm_limit_reached(script: str) -> bool:
    length = len(b64encode(script.encode('utf_16_le')))
    return length > 8192

def invoke_remote_script_uuid(authority_instance_uuid: str, script: str) -> RemoteResult:
    authority_instance = AuthorityInstance.objects.get(uuid=authority_instance_uuid)
    return invoke_remote_script(authority_instance, script)

def invoke_remote_script(authority_instance: AuthorityInstance, script: str) -> RemoteResult:
    remoting_protocol = RemotingProtocol.PSRP if winrm_limit_reached(script) else RemotingProtocol.WINRM

    if ADCS_POOL_ENABLED:
        pool = global_pool_manager.get_pool(authority_instance, remoting_protocol)

        # optimistic run; if it explodes with a transport/session error, retry once with a fresh session
        try:
            with pool.borrow() as session:
                return session.run_ps(script)
        except Exception as e1:
            logger.warning("Session likely unhealthy; retrying once with a new session: %s", e1, exc_info=True)
            # Force-create a new session by temporarily bypassing the idle queue
            s = pool.force_new()

            try:
                result = s.run_ps(script)
            finally:
                pool.release(s)
            return result
    else:
        if remoting_protocol == RemotingProtocol.WINRM:
            session = create_winrm_session_from_authority_instance(authority_instance)
        elif remoting_protocol == RemotingProtocol.PSRP:
            session = create_psrp_session_from_authority_instance(authority_instance)

        session.connect()
        result = session.run_ps(script)
        session.disconnect()
        return result
