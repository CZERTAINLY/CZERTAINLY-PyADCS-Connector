import json


def _get_any(d, *keys, default=None):
    for k in keys:
        if k in d:
            return d[k]
    return default


class ParseResult:
    def __init__(self, template, certificate):
        self.template = template
        self.certificate = certificate


class IdentifiedCertificate:
    def __init__(self, certificate_template, serial_number, config_string):
        self.certificate_template = certificate_template
        self.serial_number = serial_number
        self.config_string = config_string


class TemplateData:
    def __init__(self, name, display_name, schema_version, version, oid):
        self.name = name
        self.display_name = display_name
        self.schema_version = schema_version
        self.version = version
        self.oid = oid

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "schema_version": self.schema_version,
            "version": self.version,
            "oid": self.oid
        }

    @staticmethod
    def from_dict(template):
        return TemplateData(
            name=_get_any(template, "name", "Name"),
            display_name=_get_any(template, "display_name", "DisplayName"),
            schema_version=_get_any(template, "schema_version", "SchemaVersion"),
            version=_get_any(template, "version", "Version"),
            oid=_get_any(template, "oid", "OID"),
        )

    @staticmethod
    def from_dicts(templates):
        template_data = []
        for template in templates:
            template_data.append(TemplateData.from_dict(template))
        return template_data


class AuthorityData:
    def __init__(self, name, display_name, computer_name, config_string, ca_type, is_enterprise, is_root,
                 is_accessible, service_status):
        self.name = name
        self.display_name = display_name
        self.computer_name = computer_name
        self.config_string = config_string
        self.ca_type = ca_type
        self.is_enterprise = is_enterprise
        self.is_root = is_root
        self.is_accessible = is_accessible
        self.service_status = service_status

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "computer_name": self.computer_name,
            "config_string": self.config_string,
            "ca_type": self.ca_type,
            "is_enterprise": self.is_enterprise,
            "is_root": self.is_root,
            "is_accessible": self.is_accessible,
            "service_status": self.service_status
        }

    @staticmethod
    def from_dict(authority):
        return AuthorityData(
            name=_get_any(authority, "name", "Name"),
            display_name=_get_any(authority, "display_name", "DisplayName"),
            computer_name=_get_any(authority, "computer_name", "ComputerName"),
            config_string=_get_any(authority, "config_string", "ConfigString"),
            ca_type=_get_any(authority, "ca_type", "Type", "type"),
            is_enterprise=bool(_get_any(authority, "is_enterprise", "IsEnterprise", default=False)),
            is_root=bool(_get_any(authority, "is_root", "IsRoot", default=False)),
            is_accessible=bool(_get_any(authority, "is_accessible", "IsAccessible", default=False)),
            service_status=_get_any(authority, "service_status", "ServiceStatus"),
        )

    @staticmethod
    def from_dicts(authorities):
        authority_data = []
        for authority in authorities:
            authority_data.append(AuthorityData.from_dict(authority))
        return authority_data


def _safe_json_loads(std_out_bytes):
    text = std_out_bytes.decode("utf-8", errors="replace").strip()
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Some PowerShell cmdlets may emit warnings/noise;
        # try to find the first JSON array/object region.
        first_brace = text.find("{")
        first_bracket = text.find("[")
        idxs = [i for i in [first_brace, first_bracket] if i != -1]
        if not idxs:
            return []
        start = min(idxs)
        try:
            data = json.loads(text[start:])
        except Exception:
            return []
    # Normalize: always return a list for arrays, or list with single object
    if isinstance(data, list):
        return data
    return [data]


class DumpParser:
    @staticmethod
    def parse_certificates(input_data):
        records = _safe_json_loads(input_data.std_out)
        results = []
        for r in records:
            template = r.get("CertificateTemplate") or ""
            cert_b64 = r.get("RawCertificate") or ""
            results.append(ParseResult(template, cert_b64))
        return results

    @staticmethod
    def parse_certificates_text(input_data):
        input_string = input_data.std_out.decode("utf-8", errors="replace")
        lines = input_string.strip().split('\n')
        result = []
        in_cert = False
        cert = []
        template = ""

        for line in lines:
            if in_cert and line.startswith("      "):
                cert.append(line.strip())
            elif line.startswith("CertificateTemplate "):  # the space is important
                template = get_value_from_line(line)
            elif line.startswith("RawCertificate "):
                # first line
                cert.append(get_value_from_line(line))
                in_cert = True
            else:
                if in_cert:
                    # cert_data = "-----BEGIN CERTIFICATE-----\n" + "\n".join(cert) + "\n-----END CERTIFICATE-----"
                    cert_data = ("".join(cert)
                                 .replace("-----BEGIN CERTIFICATE-----", "")
                                 .replace("-----END CERTIFICATE-----", "")
                                 .replace("\r", "")
                                 .replace("\n", ""))
                    result.append(ParseResult(template, cert_data))
                    cert = []
                    template = ""
                in_cert = False

        return result

    @staticmethod
    def parse_identified_certificates(input_data):
        records = _safe_json_loads(input_data.std_out)
        out = []
        for r in records:
            out.append(
                IdentifiedCertificate(
                    certificate_template=r.get("CertificateTemplate") or "",
                    serial_number=r.get("SerialNumber") or "",
                    config_string=r.get("ConfigString") or "",
                )
            )
        return out

    @staticmethod
    def parse_identified_certificates_text(input_data):
        input_string = input_data.std_out.decode("utf-8", errors="replace")
        lines = input_string.strip().split('\n')
        result = []
        complete_record = False
        serial_number = ""
        certificate_template = ""
        config_string = ""

        for line in lines:
            if line.startswith("SerialNumber "):
                serial_number = get_value_from_line(line)
            elif line.startswith("CertificateTemplate "):
                certificate_template = get_value_from_line(line)
            elif line.startswith("ConfigString "):
                config_string = get_value_from_line(line)
                complete_record = True

            if complete_record:
                result.append(IdentifiedCertificate(certificate_template, serial_number, config_string))
                serial_number = ""
                certificate_template = ""
                config_string = ""
                complete_record = False

        return result

    @staticmethod
    def parse_template_data(input_data):
        records = _safe_json_loads(input_data.std_out)
        return TemplateData.from_dicts(records)

    @staticmethod
    def parse_template_data_text(input_data):
        input_string = input_data.std_out.decode("utf-8", errors="replace")
        lines = input_string.strip().split('\n')
        result = []
        complete_record = False
        name = ""
        display_name = ""
        schema_version = ""
        version = ""
        oid = ""

        for line in lines:
            if line.startswith("Name "):
                name = get_value_from_line(line)
            elif line.startswith("DisplayName "):
                display_name = get_value_from_line(line)
            elif line.startswith("SchemaVersion "):
                schema_version = get_value_from_line(line)
            elif line.startswith("Version "):
                version = get_value_from_line(line)
            elif line.startswith("OID "):
                oid = get_value_from_line(line)
                complete_record = True

            if complete_record:
                result.append(TemplateData(name, display_name, schema_version, version, oid))
                name = ""
                display_name = ""
                schema_version = ""
                version = ""
                oid = ""
                complete_record = False

        return result

    @staticmethod
    def parse_authority_data(input_data):
        records = _safe_json_loads(input_data.std_out)
        return AuthorityData.from_dicts(records)

    @staticmethod
    def parse_authority_data_text(input_data):
        input_string = input_data.std_out.decode("utf-8", errors="replace")
        lines = input_string.strip().split('\n')
        result = []
        complete_record = False
        name = ""
        display_name = ""
        computer_name = ""
        config_string = ""
        ca_type = ""
        is_enterprise = ""
        is_root = ""
        is_accessible = ""
        service_status = ""

        for line in lines:
            if line.startswith("Name "):
                name = get_value_from_line(line)
            elif line.startswith("DisplayName "):
                display_name = get_value_from_line(line)
            elif line.startswith("ComputerName "):
                computer_name = get_value_from_line(line)
            elif line.startswith("ConfigString "):
                config_string = get_value_from_line(line)
            elif line.startswith("Type "):
                ca_type = get_value_from_line(line)
            elif line.startswith("IsEnterprise "):
                is_enterprise = eval(get_value_from_line(line))
            elif line.startswith("IsRoot "):
                is_root = eval(get_value_from_line(line))
            elif line.startswith("IsAccessible "):
                is_accessible = eval(get_value_from_line(line))
            elif line.startswith("ServiceStatus "):
                service_status = get_value_from_line(line)
                complete_record = True

            if complete_record:
                result.append(AuthorityData(
                    name, display_name, computer_name, config_string, ca_type, is_enterprise, is_root,
                    is_accessible, service_status))
                name = ""
                display_name = ""
                computer_name = ""
                config_string = ""
                ca_type = ""
                is_enterprise = ""
                is_root = ""
                is_accessible = ""
                service_status = ""
                complete_record = False

        return result


def get_value_from_line(line):
    _, value = map(str.strip, line.split(":", 1))
    return value
