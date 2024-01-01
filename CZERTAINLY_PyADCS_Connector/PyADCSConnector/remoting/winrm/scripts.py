from typing import List

from PyADCSConnector.utils.dump_parser import AuthorityData, TemplateData
from PyADCSConnector.utils.revocation_reason import CertificateRevocationReason

IMPORT_MODULE = "Import-Module PSPKI"


def verify_connection_script():
    return '\n'.join([
        IMPORT_MODULE,
        "Get-CertificationAuthority | Ping-ICertInterface"
    ])


def get_cas_script():
    return '\n'.join([
        IMPORT_MODULE,
        "Get-CertificationAuthority | Format-List *",
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


def select_objects(command, property):
    if not property:
        raise ValueError("Empty property is not a valid command.")

    properties = ", ".join(property)
    return f"{command} | Select-Object -Property {properties}"


def dump_certificates_script(ca: AuthorityData, template: TemplateData, issued_after, page, page_size):
    commands = [IMPORT_MODULE]
    if issued_after:
        commands.append(f'$issued_after = Get-Date -Date "{issued_after}"')
    base_cmd = (f'Get-CertificationAuthority -Name "{ca.name}" | Get-IssuedRequest -Property "RawCertificate"'
                f' -Page {page} -PageSize {page_size} -Filter "Request.Disposition -ge 12",'
                f' "Request.Disposition -le 21"')
    if not template:
        base_cmd = base_cmd
    else:
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
        f"Get-CertificationAuthority -Name \"{ca.name}\" | Get-IssuedRequest -Filter \"SerialNumber -eq {serial_number}\""
    ])


def get_revoke_script(ca: AuthorityData, certificate_serial_number: str, reason: str) -> str:
    adcs_reason = CertificateRevocationReason.from_string(reason).to_string_ps_value()

    return '\n'.join([
        IMPORT_MODULE,
        f"Get-CertificationAuthority -Name \"{ca.name}\" | Get-IssuedRequest -Filter"
        f" \"SerialNumber -eq {certificate_serial_number}\" | Revoke-Certificate -Reason \"{adcs_reason}\""
    ])
