import logging

from psrp import WSManInfo, SyncRunspacePool, SyncPowerShell
from psrpcore.types import RunspacePoolState

from PyADCSConnector.exceptions.psrp_execution_exception import PsrpExecutionException
from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.remoting.remote_result import RemoteResult
from PyADCSConnector.utils import attribute_definition_utils

logger = logging.getLogger(__name__)


class PsrpRemoting(object):
    def __init__(self, username, password, hostname, use_https=False, port=5985, transport='credssp'):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.use_https = use_https
        self.port = port
        self.transport = transport
        self.protocol = None

    def connect(self):
        wsman_info = WSManInfo(
            server=self.hostname ,
            username=self.username,
            password=self.password,
            port=self.port,
            scheme="https" if self.use_https else "http",
            # convert self.transport to Literal
            auth=self.transport if self.transport in ["credssp", "kerberos", "basic", "negotiate"] else "credssp",
        )
        self.protocol = SyncRunspacePool(wsman_info)
        self.protocol.open()

    def run_ps(self, script):
        if not self.protocol or self.protocol.state != RunspacePoolState.Opened:
            raise Exception("Runspace pool is not opened. Please connect first.")

        logger.debug("Running command: " + script)

        ps = SyncPowerShell(self.protocol)
        ps.add_script(script)

        try:
            result = ps.invoke()
        except Exception as e:
            logger.exception("PSRP transport/protocol failure")
            raise PsrpExecutionException(-1, f"Transport/protocol error: {e}") from e

        # Convert outputs to text
        stdout_text = "\n".join(str(o) for o in (result or []))

        err_recs = []
        if ps.streams and ps.streams.error:
            for er in ps.streams.error:
                exc = getattr(er, "exception", None)
                msg = getattr(exc, "message", None) if exc else None
                err_recs.append({
                    "Message": msg or str(er),
                    "FullyQualifiedErrorId": getattr(er, "fully_qualified_error_id", None)
                                             or getattr(er, "fully_qualified_id", None),
                    "CategoryInfo": str(getattr(er, "category_info", None)),
                    "ScriptStackTrace": getattr(er, "script_stack_trace", None),
                    "InvocationInfo": str(getattr(er, "invocation_info", None)),
                })

        stderr_text = "\n".join((d["Message"] or "") for d in err_recs)

        had_errors = bool(err_recs)
        if had_errors:
            logger.error("PowerShell errors: %r", err_recs)

        logger.debug("PowerShell output:\n%s", stdout_text)

        return RemoteResult(
            status_code=1 if had_errors else 0,
            std_out=stdout_text.encode("utf-8"),
            std_err=stderr_text.encode("utf-8"),
            had_errors=had_errors,
        )

    def disconnect(self):
        if self.protocol and self.protocol.state == RunspacePoolState.Opened:
            self.protocol.close()
            self.protocol = None

def check_result(result):
    if result.had_errors:
        raise PsrpExecutionException(result.status_code, result.std_err.decode('utf-8'))

def create_psrp_session_from_authority_instance_uuid(authority_instance_uuid):
    authority_instance = AuthorityInstance.objects.get(uuid=authority_instance_uuid)
    return create_psrp_session_from_authority_instance(authority_instance)


def create_psrp_session_from_authority_instance(authority_instance):
    username = attribute_definition_utils.get_attribute_value("username",
                                                              authority_instance.credential.get("attributes"))
    password = attribute_definition_utils.get_attribute_value("password",
                                                              authority_instance.credential.get("attributes"))

    # check if password is in the form { "secret": "password" } and if yes, extract the password only
    # this is related to the change in the CZERTAINLY version 2.12.0
    if isinstance(password, dict):
        password = password.get("secret")

    session = PsrpRemoting(username, password, authority_instance.address, authority_instance.https,
                            authority_instance.port)
    return session