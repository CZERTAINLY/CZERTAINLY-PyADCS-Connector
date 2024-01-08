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
        template_data = TemplateData(
            name=template["name"],
            display_name=template["display_name"],
            schema_version=template["schema_version"],
            version=template["version"],
            oid=template["oid"])
        return template_data

    @staticmethod
    def from_dicts(templates):
        template_data = []
        for template in templates:
            template_data.append(TemplateData.from_dict(template))
        return template_data


class AuthorityData:
    def __init__(self, name, display_name, computer_name, config_string, ca_type, is_enterprise, is_root):
        self.name = name
        self.display_name = display_name
        self.computer_name = computer_name
        self.config_string = config_string
        self.ca_type = ca_type
        self.is_enterprise = is_enterprise
        self.is_root = is_root

    def to_dict(self):
        return {
            "name": self.name,
            "display_name": self.display_name,
            "computer_name": self.computer_name,
            "config_string": self.config_string,
            "ca_type": self.ca_type,
            "is_enterprise": self.is_enterprise,
            "is_root": self.is_root
        }

    @staticmethod
    def from_dict(authority):
        authority_data = AuthorityData(
            name=authority["name"],
            display_name=authority["display_name"],
            computer_name=authority["computer_name"],
            config_string=authority["config_string"],
            ca_type=authority["ca_type"],
            is_enterprise=authority["is_enterprise"],
            is_root=authority["is_root"])
        return authority_data

    @staticmethod
    def from_dicts(authorities):
        authority_data = []
        for authority in authorities:
            authority_data.append(AuthorityData.from_dict(authority))
        return authority_data


class DumpParser:
    @staticmethod
    def parse_certificates(input_data):
        input_string = input_data.std_out.decode('utf-8')
        lines = input_string.strip().split('\n')
        result = []
        in_cert = False
        cert = []
        template = ""

        for line in lines:
            if in_cert and line.startswith("                         "):
                cert.append(line.strip())
            elif line.startswith("CertificateTemplate        : "):
                template = DumpParser.parse_template_name(line)
            elif line.startswith("RawCertificate             : "):
                # first line
                cert.append(line.replace("RawCertificate             : ", "").strip())
                in_cert = True
            else:
                if in_cert:
                    cert_data = "-----BEGIN CERTIFICATE-----\n" + "\n".join(cert) + "\n-----END CERTIFICATE-----"
                    result.append(ParseResult(template, cert_data))
                    cert = []
                    template = ""
                in_cert = False

        return result

    @staticmethod
    def parse_identified_certificates(input_data):
        input_string = input_data.std_out.decode('utf-8')
        lines = input_string.strip().split('\n')
        result = []
        complete_record = False
        serial_number = ""
        certificate_template = ""
        config_string = ""

        for line in lines:
            if line.startswith("SerialNumber               : "):
                serial_number = line.replace("SerialNumber               : ", "").strip()
            elif line.startswith("CertificateTemplate        : "):
                certificate_template = line.replace("CertificateTemplate        : ", "").strip()
            elif line.startswith("ConfigString               : "):
                config_string = line.replace("ConfigString               : ", "").strip()
                complete_record = True

            if complete_record:
                result.append(IdentifiedCertificate(certificate_template, serial_number, config_string))
                serial_number = ""
                certificate_template = ""
                config_string = ""
                complete_record = False

        return result

    @staticmethod
    def parse_template_name(line):
        return line.replace("CertificateTemplate        : ", "").strip()

    @staticmethod
    def parse_template_data(input_data):
        input_string = input_data.std_out.decode('utf-8')
        lines = input_string.strip().split('\n')
        result = []
        complete_record = False
        name = ""
        display_name = ""
        schema_version = ""
        version = ""
        oid = ""

        for line in lines:
            if line.startswith("Name          : "):
                name = line.replace("Name          : ", "").strip()
            elif line.startswith("DisplayName   : "):
                display_name = line.replace("DisplayName   : ", "").strip()
            elif line.startswith("SchemaVersion : "):
                schema_version = line.replace("SchemaVersion : ", "").strip()
            elif line.startswith("Version       : "):
                version = line.replace("Version       : ", "").strip()
            elif line.startswith("OID           : "):
                oid = line.replace("OID           : ", "").strip()
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
        input_string = input_data.std_out.decode('utf-8')
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

        for line in lines:
            if line.startswith("Name                 : "):
                name = line.replace("Name                 : ", "").strip()
            elif line.startswith("DisplayName          : "):
                display_name = line.replace("DisplayName          : ", "").strip()
            elif line.startswith("ComputerName         : "):
                computer_name = line.replace("ComputerName         : ", "").strip()
            elif line.startswith("ConfigString         : "):
                config_string = line.replace("ConfigString         : ", "").strip()
            elif line.startswith("Type                 : "):
                ca_type = line.replace("Type                 : ", "").strip()
            elif line.startswith("IsEnterprise         : "):
                is_enterprise = eval(line.replace("IsEnterprise         : ", "").strip())
            elif line.startswith("IsRoot               : "):
                is_root = eval(line.replace("IsRoot               : ", "").strip())
                complete_record = True

            if complete_record:
                result.append(AuthorityData(
                    name, display_name, computer_name, config_string, ca_type, is_enterprise, is_root))
                name = ""
                display_name = ""
                computer_name = ""
                config_string = ""
                ca_type = ""
                is_enterprise = ""
                is_root = ""
                complete_record = False

        return result
