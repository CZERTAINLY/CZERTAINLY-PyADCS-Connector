from PyADCSConnector.utils.dump_parser import AuthorityData, TemplateData
from PyADCSConnector.utils.revocation_reason import CertificateRevocationReason

IMPORT_MODULE = """Import-Module PSPKI
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$Host.UI.RawUI.BufferSize = New-Object Management.Automation.Host.Size (2048, $Host.UI.RawUI.BufferSize.Height)"""


def verify_connection_script():
    """
    Returns a script that verifies the connection to the remote server.
    """
    return '\n'.join([
        IMPORT_MODULE,
        # "Get-CertificationAuthority | Ping-ICertInterface"
    ])


def get_ca_script(computer_name: str):
    return '\n'.join([
        IMPORT_MODULE,
        "Get-CertificationAuthority -ComputerName " + computer_name + " | Format-List *",
    ])


def get_cas_script():
    return '\n'.join([
        IMPORT_MODULE,
        "$TemplateList = @()",
        "(Get-CertificationAuthority) | Foreach-Object {",
        "$template = $_",
        "$OutputObject = \"\" | Select Name, DisplayName, ComputerName, ConfigString, Type, IsEnterprise, IsRoot, "
        "IsAccessible, ServiceStatus",
        "$outputObject.Name = $template.Name",
        "$OutputObject.DisplayName = $template.DisplayName",
        "$OutputObject.ComputerName = $template.ComputerName",
        "$OutputObject.ConfigString = $template.ConfigString",
        "$OutputObject.Type = $template.Type",
        "$OutputObject.IsEnterprise = $template.IsEnterprise",
        "$OutputObject.IsRoot = $template.IsRoot",
        "$OutputObject.IsAccessible = $template.IsAccessible",
        "$OutputObject.ServiceStatus = $template.ServiceStatus",
        "$TemplateList += $OutputObject",
        "}",
        "$TemplateList | Format-List"
    ])


def get_templates_script():
    return '\n'.join([
        IMPORT_MODULE,
        "$TemplateList = @()",
        "(Get-CertificateTemplate) | Foreach-Object {",
        "$template = $_",
        "$OutputObject = \"\" | Select Name, DisplayName, SchemaVersion, Version, OID",
        "$outputObject.Name = $template.Name",
        "$OutputObject.DisplayName = $template.DisplayName",
        "$OutputObject.SchemaVersion = $template.SchemaVersion",
        "$OutputObject.Version = $template.Version",
        "$OutputObject.OID = $template.Oid.Value",
        "$TemplateList += $OutputObject",
        "}",
        "$TemplateList | Format-List"
    ])


def select_objects(command, select_property):
    if not select_property:
        raise ValueError("Empty property is not a valid command.")

    properties = ", ".join(select_property)
    return f"{command} | Select-Object -Property {properties}"


def dump_certificates_script(ca: AuthorityData, template: TemplateData or None, issued_after, page, page_size):
    commands = [IMPORT_MODULE]
    if issued_after:
        commands.append(f'$issued_after = Get-Date -Date "{issued_after}"')
    base_cmd = (f'Get-CertificationAuthority -Name "{ca.name}" | Get-AdcsDatabaseRow -Property "RawCertificate"'
                f' -Page {page} -PageSize {page_size} -Filter "Request.Disposition -ge 12",'
                f' "Request.Disposition -le 21"')
    if template:
        if template.schema_version == "1":
            base_cmd = f'{base_cmd}, "CertificateTemplate -eq {template.name}"'
        else:
            base_cmd = f'{base_cmd}, "CertificateTemplate -eq {template.oid}"'

    if issued_after:
        commands.append(f'{base_cmd}, "NotBefore -ge $issued_after"')
    else:
        commands.append(base_cmd)

    return '\n'.join(commands)


def submit_certificate_request_script(request, ca: AuthorityData, template: TemplateData):
    return '\n'.join([
        IMPORT_MODULE,
        f"$req = \"{request}\"",
        "$CertRequest = New-Object -ComObject CertificateAuthority.Request",
        f"$Status = $CertRequest.Submit(0xff, $req, \"CertificateTemplate:{template.name}\", \"{ca.config_string}\")",
        f"$cert = Get-CertificationAuthority -Name \"{ca.name}\" | Get-IssuedRequest -RequestID "
        f"$CertRequest.GetRequestId() -Property \"RawCertificate\"",
        "$cert.RawCertificate"
    ])


def get_template_oid_script(template):
    return '\n'.join([
        IMPORT_MODULE,
        f"(Get-CertificateTemplate -Name \"{template}\").Oid.Value"
    ])


def identify_certificate_script(serial_number, ca: AuthorityData):
    return '\n'.join([
        IMPORT_MODULE,
        f'Get-CertificationAuthority -Name "{ca.name}" | Get-AdcsDatabaseRow'
        f' -Filter "SerialNumber -eq {serial_number}", "Request.Disposition -ge 12", "Request.Disposition -le 21"'
        f' -Property "SerialNumber", "CertificateTemplate", "ConfigString"'
        # getting only issued requests without revoked ones
        # f'Get-CertificationAuthority -Name "{ca.name}" | Get-IssuedRequest'
        # f' -Filter "SerialNumber -eq {serial_number}"'
    ])


def get_revoke_script(ca: AuthorityData, certificate_serial_number: str, reason: str) -> str:
    adcs_reason = CertificateRevocationReason.from_string(reason).to_string_ps_value()

    return '\n'.join([
        IMPORT_MODULE,
        f"Get-CertificationAuthority -Name \"{ca.name}\" | Get-IssuedRequest -Filter"
        f" \"SerialNumber -eq {certificate_serial_number}\" | Revoke-Certificate -Reason \"{adcs_reason}\""
    ])
