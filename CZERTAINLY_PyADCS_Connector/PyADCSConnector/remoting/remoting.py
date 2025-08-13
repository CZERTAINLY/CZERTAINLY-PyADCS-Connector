import logging
from base64 import b64encode

from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.remoting.pool_manager import global_pool_manager
from PyADCSConnector.remoting.remote_result import RemoteResult
from PyADCSConnector.remoting.remoting_protocol import RemotingProtocol

logger = logging.getLogger(__name__)

def winrm_limit_reached(script: str) -> bool:
    length = len(b64encode(script.encode('utf_16_le')))
    return length > 8192

def invoke_remote_script_uuid(authority_instance_uuid: str, script: str) -> RemoteResult:
    authority_instance = AuthorityInstance.objects.get(uuid=authority_instance_uuid)
    return invoke_remote_script(authority_instance, script)

def invoke_remote_script(authority_instance: AuthorityInstance, script: str) -> RemoteResult:
    # decide protocol exactly as you already do
    remoting_protocol = RemotingProtocol.PSRP if winrm_limit_reached(script) else RemotingProtocol.WINRM

    # borrow from the appropriate pool (created lazily on first access)
    pool = global_pool_manager.get_pool(authority_instance, remoting_protocol)

    # borrow() blocks when the pool is at capacity and releases on context exit
    with pool.borrow() as session:
        return session.run_ps(script)
