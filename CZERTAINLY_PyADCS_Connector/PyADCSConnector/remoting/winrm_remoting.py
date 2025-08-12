import base64
import gzip
import logging
import re
from base64 import b64encode

import winrm

from PyADCSConnector.exceptions.winrm_execution_exception import WinRMExecutionException
from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.utils import attribute_definition_utils

logger = logging.getLogger(__name__)


BOOTSTRAP = r"""
$B = '<B64>';
$ms = New-Object IO.MemoryStream(,[Convert]::FromBase64String($B))
$gs = New-Object IO.Compression.GzipStream($ms,[IO.Compression.CompressionMode]::Decompress)
$sr = New-Object IO.StreamReader($gs,[Text.Encoding]::UTF8)
$code = $sr.ReadToEnd(); $sr.Close(); $gs.Close(); $ms.Close()
iex $code
"""

import re

def minify_ps(script: str) -> str:
    """
    Aggressive PowerShell minifier:
    - removes comments (# ... and <# ... #>)
    - keeps whitespace inside quotes
    - collapses whitespace outside quotes
    - joins lines with ';' when safe (heuristic)
    """
    s = script

    # 1) Remove block comments: <# ... #>
    s = re.sub(r'<#.*?#>', '', s, flags=re.S)

    # 2) Remove whole-line comments (start-of-line or after leading spaces)
    s = re.sub(r'(?m)^[ \t]*#.*$', '', s)

    # 3) Trim trailing spaces
    s = re.sub(r'[ \t]+(?=\n)', '', s)

    # 4) Remove empty lines
    s = re.sub(r'(?m)^\s*\n', '', s)

    # 5) Collapse runs of spaces/tabs outside quoted strings
    #    This regex splits into quoted vs non-quoted chunks and only collapses in the non-quoted parts.
    def _collapse_ws(m):
        text = m.group(0)
        if text.startswith('"') or text.startswith("'"):
            return text  # inside string: leave as-is
        # outside string: collapse multiple spaces/tabs to single space
        text = re.sub(r'[ \t]{2,}', ' ', text)
        return text

    s = re.sub(
        r"""
        (?:'[^'\\]*(?:\\.[^'\\]*)*')     |   # single-quoted string (rough)
        (?:"[^"\\]*(?:\\.[^"\\]*)*")     |   # double-quoted string (rough)
        [^'"]+                               # non-quoted text
        """,
        _collapse_ws,
        s,
        flags=re.S | re.X
    )

    # 6) Split to logical lines and join with ';' when it looks safe.
    #    Heuristics: don't join if prev ends with {, |, `, or ,  / or if current starts with }
    lines = [ln.strip() for ln in s.splitlines() if ln.strip()]
    out = []
    for i, ln in enumerate(lines):
        out.append(ln)
        if i == len(lines) - 1:
            break
        nxt = lines[i + 1]
        prev = ln

        end = prev[-1]
        # Don’t add semicolon if previous line ends with these continuation chars
        if end in ('{', '|', '`', ','):
            continue
        # Don’t put semicolon before a closing brace
        if nxt.startswith('}'):
            continue
        # If previous line already ends with ';', skip
        if end == ';':
            continue
        out.append(';')

    return ''.join(out).strip()


def ps_gzip_b64(s: str) -> str:
    return base64.b64encode(gzip.compress(s.encode('utf_16_le'))).decode('ascii')


class WinRmRemoting(object):
    def __init__(self, username, password, hostname, use_https=False, port=5985, transport='credssp'):
        self.shell_id = None
        self.username = username
        self.password = password
        self.hostname = hostname
        self.use_https = use_https
        self.port = port
        self.transport = transport
        self.protocol = None

    def connect(self):
        self.protocol = winrm.Protocol(
            endpoint='http' + ('s' if self.use_https else '') + '://' + self.hostname + ':' + str(self.port) + '/wsman',
            transport=self.transport,
            username=self.username,
            password=self.password)
        self.shell_id = self.protocol.open_shell()

    def run(self, command, args=()):
        logger.debug("Running command: " + command + " " + str(args))
        command_id = self.protocol.run_command(self.shell_id, command, args)
        result = winrm.Response(self.protocol.get_command_output(self.shell_id, command_id))
        self.protocol.cleanup_command(self.shell_id, command_id)

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Return code: " + str(result.status_code))
            if result.status_code != 0:
                logger.debug("Error: " + result.std_err.decode(encoding='utf-8'))
            else:
                logger.debug("Output: " + result.std_out.decode(encoding='utf-8'))

        check_result(result)
        return result

    def run_ps(self, script):
        """base64 encodes a Powershell script and executes the powershell encoded script command"""
        logger.debug("Running Powershell script: " + script)
        # must use utf16 little endian on windows
        encoded_ps = b64encode(script.encode('utf_16_le')).decode('ascii')
        result = self.run('powershell -encodedcommand {0}'.format(encoded_ps))
        return result

    def run_long_ps(self, script):
        ps_to_send = BOOTSTRAP.replace("<B64>", ps_gzip_b64(minify_ps(script)))
        result = self.run_ps(ps_to_send)
        return result

    def disconnect(self):
        self.protocol.close_shell(self.shell_id)
        self.protocol = None
        self.shell_id = None


def check_result(result):
    if result.status_code != 0:
        raise WinRMExecutionException(result.status_code, result.std_err.decode('utf-8'))


def create_session_from_authority_instance_name(authority_instance_name):
    authority_instance = AuthorityInstance.objects.get(name=authority_instance_name)
    return create_session_from_authority_instance(authority_instance)


def create_session_from_authority_instance_uuid(authority_instance_uuid):
    authority_instance = AuthorityInstance.objects.get(uuid=authority_instance_uuid)
    return create_session_from_authority_instance(authority_instance)


def create_session_from_authority_instance(authority_instance):
    username = attribute_definition_utils.get_attribute_value("username",
                                                              authority_instance.credential.get("attributes"))
    password = attribute_definition_utils.get_attribute_value("password",
                                                              authority_instance.credential.get("attributes"))

    # check if password is in the form { "secret": "password" } and if yes, extract the password only
    # this is related to the change in the CZERTAINLY version 2.12.0
    if isinstance(password, dict):
        password = password.get("secret")

    session = WinRmRemoting(username, password, authority_instance.address, authority_instance.https,
                            authority_instance.port)
    return session
