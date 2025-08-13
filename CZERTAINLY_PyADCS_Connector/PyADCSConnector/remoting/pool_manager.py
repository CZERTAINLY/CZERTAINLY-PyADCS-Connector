import logging
import threading
from typing import Dict, Tuple

from CZERTAINLY_PyADCS_Connector.settings import ADCS_POOL_MAX_SIZE, ADCS_POOL_MIN_WARM_SIZE, \
    ADCS_POOL_KEEPALIVE_INTERVAL, ADCS_POOL_MAX_IDLE_SECONDS
from PyADCSConnector.remoting.psrp_remoting import create_psrp_session_from_authority_instance
from PyADCSConnector.remoting.remoting_protocol import RemotingProtocol
from PyADCSConnector.remoting.session_adapters import WinRMAdapter, PSRPAdapter
from PyADCSConnector.remoting.session_pool import SessionPool
from PyADCSConnector.remoting.winrm_remoting import create_winrm_session_from_authority_instance
from PyADCSConnector.utils import attribute_definition_utils

logger = logging.getLogger(__name__)


class PoolManager:
    def __init__(self, *, maxsize=8, min_warm=1, keepalive_interval_s=25, max_idle_s=600):
        self._lock = threading.Lock()
        self._pools: Dict[Tuple, SessionPool] = {}
        self._cfg = {
            "maxsize": maxsize,
            "min_warm": min_warm,
            "keepalive_interval_s": keepalive_interval_s,
            "max_idle_s": max_idle_s,
        }

    def _get_attr(self, authority_instance, name: str, default=None):
        cred = getattr(authority_instance, "credential", None) or {}
        attrs = cred.get("attributes") if isinstance(cred, dict) else None
        try:
            return attribute_definition_utils.get_attribute_value(name, attrs)
        except Exception:
            return default

    def get_pool(self, authority_instance, protocol: RemotingProtocol) -> SessionPool:
        # Pull values from attributes list safely
        username = self._get_attr(authority_instance, "username", default=None)
        transport = (
            self._get_attr(authority_instance, "transport", default=None)
            or getattr(authority_instance, "transport", None)
            or "credssp"
        )

        # Build a stable key per destination + protocol + auth context
        key = (
            protocol,
            authority_instance.address,
            authority_instance.port,
            bool(authority_instance.https),
            username,
            transport,
        )

        with self._lock:
            pool = self._pools.get(key)
            if pool:
                return pool

            if protocol == RemotingProtocol.WINRM:
                def _factory():
                    sess = create_winrm_session_from_authority_instance(authority_instance)
                    return WinRMAdapter(sess, key)
                name = f"winrm://{authority_instance.address}:{authority_instance.port}"
            else:
                def _factory():
                    sess = create_psrp_session_from_authority_instance(authority_instance)
                    return PSRPAdapter(sess, key)
                name = f"psrp://{authority_instance.address}:{authority_instance.port}"

            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"Creating new session pool for {name} with key {key} and config {self._cfg}")

            pool = SessionPool(factory=_factory, name=name, **self._cfg)
            self._pools[key] = pool
            return pool


# singleton
global_pool_manager = PoolManager(
    maxsize=ADCS_POOL_MAX_SIZE,
    min_warm=ADCS_POOL_MIN_WARM_SIZE,
    keepalive_interval_s=ADCS_POOL_KEEPALIVE_INTERVAL,
    max_idle_s=ADCS_POOL_MAX_IDLE_SECONDS,
)
