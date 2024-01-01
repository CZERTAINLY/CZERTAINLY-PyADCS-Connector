import winrm
from django.test import TestCase

from PyADCSConnector.utils.dump_parser import DumpParser


class DumpParserTest(TestCase):
    def test_parse_certificates(self):
        data = """

RequestID              : 92
Request.RequesterName  : 3KEY\\nejaky.uzivatel
CommonName             : stolin.cloudfield.cz
NotBefore              : 9/14/2021 10:29:04 AM
NotAfter               : 9/14/2023 10:29:04 AM
SerialNumber           : 180000005c361831d4fb7ac06f00000000005c
CertificateTemplate    : WebServer
RawCertificate         : MIIFqjCCA5KgAwIBAgITGAAAAFw2GDHU+3rAbwAAAAAAXDANBgkqhkiG9w0BAQ0F
                         ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                         YW55IHMuci5vLjAeFw0yMTA5MTQxMDI5MDRaFw0yMzA5MTQxMDI5MDRaMIGvMQsw
                         CQYDVQQGEwJjejEXMBUGA1UECBMOY3plY2ggcmVwdWJsaWMxFzAVBgNVBAcTDmhS
                         +aXRHaOZLWSfI96whFyOlSUbjFA/wfaM8QOFGEo6iInENJaT7c7nsL61/tGna8wT
                         1aMeYm314Hw3kyWRXbcFogODKrGlUDFfLgiZ1+7qIIYvRw0b0CUABz8kzgloF3kY
                         ez76He+xnDn84MozAhzO0dch2Db8IarlAf237SLNE6PWho0h0yOjkfur3dV5YWg3
                         fcF9OHcKpdEDR0Ne6tLiTOcCh1WTCw8ZcbP6ojbnmaZhsWo7uMxaLeCF8/dNOcI6
                         5D+2iXCq7fXq0hPbTdw=

CertificateTemplateOid : WebServer
RowId                  : 92
ConfigString           : vmi307469.3key.local\\Demo MS Sub CA
Table                  : Request
Properties             : {[RequestID, 92], [Request.RequesterName, 3KEY\\nejaky.uzivatel], [CommonName,
                         stolin.cloudfield.cz], [NotBefore, 9/14/2021 10:29:04 AM]...}

RequestID              : 93
Request.RequesterName  : 3KEY\\nejaky.uzivatel
CommonName             : stolin.cloudfield.cz
NotBefore              : 9/14/2021 10:31:55 AM
NotAfter               : 9/14/2023 10:31:55 AM
SerialNumber           : 180000005da983bee662f1644000000000005d
CertificateTemplate    : WebServer
RawCertificate         : MIIFqjCCA5KgAwIBAgITGAAAAF2pg77mYvFkQAAAAAAAXTANBgkqhkiG9w0BAQ0F
                         ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                         YW55IHMuci5vLjAeFw0yMTA5MTQxMDMxNTVaFw0yMzA5MTQxMDMxNTVaMIGvMQsw
                         CQYDVQQGEwJjejEXMBUGA1UECBMOY3plY2ggcmVwdWJsaWMxFzAVBgNVBAcTDmhS
                         QURFQyBrUkFMT1ZFMRMwEQYDVQQKEwpjbG91ZGZpZWxkMQ4wDAYDVQQLEwVhenVy
                         ZTEdMBsGA1UEAxMUc3RvbGluLmNsb3VkZmllbGQuY3oxKjAoBgkqhkiG9w0BCQEW
                         G3ZhY2xhdi5zdG9saW5AY2xvdWRmaWVsZC5jejCCASIwDQYJKoZIhvcNAQEBBQAD
                         ggEPADCCAQoCggEBAMKNY2L7xt4+PpiDk1DDXgN6fgSAXoAmepEEKhju6zezxlbq
                         jKaVLYnvBz1UV2m2Gwf+uLv+ZhmGj5tA/Q8VN4ltop0X5JG05q2Dowot3ShE/kVg
                         WAG1ckjNcJIj9kKZPpLjLYitFzVWzacAQn0NpJNYKu0gL7vizPZsBvlsB1V4MZjt
                         1cyM5fFt1CWUB/eo7GQ5Hp1h1x3oH0k7CzFDVd91nVXxEuqPQZeusVsr9bQdrUbS
                         Yp/urn13flx6r29Ff9JZOdUGD5g9Mw2IrRXkMcmnEfkMSbBbAwccImkuQ8bCuHCD
                         oMS/90/d7jDxGvB5wgZiD188VsoNj3G80VXfPUARCbmLkoA74vrt9sj4w/Sh2VAQ
                         XNhyT45tc2eaCNyxFqhr0wiIrfyI7K/sfRg8VtQf0C07gjMcmomREfFwczfvLfIx
                         GuzgIV7fd/1dMh2OsYM=

CertificateTemplateOid : WebServer
RowId                  : 93
ConfigString           : vmi307469.3key.local\\Demo MS Sub CA
Table                  : Request
Properties             : {[RequestID, 93], [Request.RequesterName, 3KEY\\nejaky.uzivatel], [CommonName,
                         stolin.cloudfield.cz], [NotBefore, 9/14/2021 10:31:55 AM]...}

RequestID              : 94
Request.RequesterName  : 3KEY\\nejaky.uzivatel
CommonName             : stolin.cloudfield.cz
NotBefore              : 9/14/2021 10:33:10 AM
NotAfter               : 9/14/2023 10:33:10 AM
SerialNumber           : 180000005e2eaba4393d43d5dd00000000005e
CertificateTemplate    : WebServer
RawCertificate         : MIIFqjCCA5KgAwIBAgITGAAAAF4uq6Q5PUPV3QAAAAAAXjANBgkqhkiG9w0BAQ0F
                         ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                         YW55IHMuci5vLjAeFw0yMTA5MTQxMDMzMTBaFw0yMzA5MTQxMDMzMTBaMIGvMQsw
                         CQYDVQQGEwJjejEXMBUGA1UECBMOY3plY2ggcmVwdWJsaWMxFzAVBgNVBAcTDmhS
                         QURFQyBrUkFMT1ZFMRMwEQYDVQQKEwpjbG91ZGZpZWxkMQ4wDAYDVQQLEwVhenVy
                         kNTOeq3IxCaLiQfu4aFlHgfkp7IcRtnf9x6tBkqbpB8wfwDRig+ueMoOdbeeNdIm
                         jNMj7SVQVjtU4PO47bmATcbqh7SaBzm6YHUitQqaeNJezRQN0KOb4McewCGavrgT
                         aGT/36EI1I1pXEXieMwVmp1gWp2AnhIVcZzeQyz12W1S3Pvade1soJlPqodcF1kB
                         7cyrotkTwFhd4BcaO38=

CertificateTemplateOid : WebServer
RowId                  : 94
ConfigString           : vmi307469.3key.local\\Demo MS Sub CA
Table                  : Request
Properties             : {[RequestID, 94], [Request.RequesterName, 3KEY\\nejaky.uzivatel], [CommonName,
                         stolin.cloudfield.cz], [NotBefore, 9/14/2021 10:33:10 AM]...}

RequestID              : 95
Request.RequesterName  : 3KEY\\nejaky.uzivatel
CommonName             : stolin.cloudfield.cz
NotBefore              : 9/14/2021 10:39:04 AM
NotAfter               : 9/14/2023 10:39:04 AM
SerialNumber           : 180000005fa28c539c099024c900000000005f
CertificateTemplate    : WebServer
RawCertificate         : MIIFqjCCA5KgAwIBAgITGAAAAF+ijFOcCZAkyQAAAAAAXzANBgkqhkiG9w0BAQ0F
                         ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                         YW55IHMuci5vLjAeFw0yMTA5MTQxMDM5MDRaFw0yMzA5MTQxMDM5MDRaMIGvMQsw
                         W8ZsV0D44UenisPFKhNes5FDRw3GvEwkCoizlrBGpgSkPLg/9BeJb3cVp7ikjN5C
                         sLX+nsMxz7LGZeHlbae5FPgDjiee01Z/GZp/MJAufa9xE/WkurljivuyAdUS0oft
                         53roGPhlRx1mzff0cYZz0LmXeJnxPAFoS4rlLl+p0OiJ1EJ6KWo/yngu54AI5ja9
                         v4QNdaSxYWL2S//baU1UvjLL+mDxeVNOK2lLUhWwbyLDLrHIn5L60itVv9z9m94X
                         XPQ/raOMDWoUaG9bZ7Yz3Gb3heNB4K21jv7NEYy19mrJahKpVd/Na0/a8OrLIcPV
                         WrV0f4o6nCLtsSc1WL8=

CertificateTemplateOid : WebServer
RowId                  : 95
ConfigString           : vmi307469.3key.local\\Demo MS Sub CA
Table                  : Request
Properties             : {[RequestID, 95], [Request.RequesterName, 3KEY\\nejaky.uzivatel], [CommonName,
                         stolin.cloudfield.cz], [NotBefore, 9/14/2021 10:39:04 AM]...}

RequestID              : 96
Request.RequesterName  : 3KEY\\nejaky.uzivatel
CommonName             : stolin.cloudfield.cz
NotBefore              : 9/14/2021 1:36:34 PM
NotAfter               : 9/14/2023 1:36:34 PM
SerialNumber           : 180000006065ba635752f7471d000000000060
CertificateTemplate    : WebServer
RawCertificate         : MIIFqjCCA5KgAwIBAgITGAAAAGBlumNXUvdHHQAAAAAAYDANBgkqhkiG9w0BAQ0F
                         ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                         YW55IHMuci5vLjAeFw0yMTA5MTQxMzM2MzRaFw0yMzA5MTQxMzM2MzRaMIGvMQsw
                         Vxmyiue5YialdjgJaF8tw25Z/kYtPWugAdmiPQokL1OAAxstMGxaQ9E6UkkA274S
                         bF0jZPGX9gmL4fZYh9zN2kg8JinkcP5013OYFuF83GRjB1o59rH5lZPufBIjQt8j
                         mE3bzH6yEgFOBjSAfpc=

CertificateTemplateOid : WebServer
RowId                  : 96
ConfigString           : vmi307469.3key.local\\Demo MS Sub CA
Table                  : Request
Properties             : {[RequestID, 96], [Request.RequesterName, 3KEY\\nejaky.uzivatel], [CommonName,
                         stolin.cloudfield.cz], [NotBefore, 9/14/2021 1:36:34 PM]...}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_certificates(result)
        self.assertEqual(len(templates), 5)
        self.assertEqual(templates[0].template, "WebServer")

    def test_parse_template(self):
        data = """
        
Name          : TestofEnrollmentAgent
DisplayName   : Test of Enrollment Agent
SchemaVersion : 4
Version       : 100.3
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.8007785.10868302

Name          : User
DisplayName   : User
SchemaVersion : 1
Version       : 3.1
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.1

Name          : UserSignature
DisplayName   : User Signature Only
SchemaVersion : 1
Version       : 4.1
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.2

Name          : WebServer
DisplayName   : Web Server
SchemaVersion : 1
Version       : 4.1
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.16

Name          : Workstation
DisplayName   : Workstation Authentication
SchemaVersion : 2
Version       : 101.0
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.30

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_template_data(result)
        self.assertEqual(len(templates), 5)
        self.assertEqual(templates[0].name, "TestofEnrollmentAgent")
        self.assertEqual(templates[1].display_name, "User")
        self.assertEqual(templates[2].schema_version, "1")
        self.assertEqual(templates[3].version, "4.1")
        self.assertEqual(templates[4].oid, "1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.30")

    def test_parse_identified_certificates(self):
        data = """

RequestID              : 710
Request.RequesterName  : 3KEY\\nejaky.uzivatel
CommonName             : Users
                         Nějaký Uživatel
NotBefore              : 7/7/2023 9:25:52 AM
NotAfter               : 7/6/2024 9:25:52 AM
SerialNumber           : 18000002c69a773092830df76a0000000002c6
CertificateTemplate    : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.2517003.8444064
CertificateTemplateOid : Certificate authentication external client
                         (1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.2517003.8444064)
RowId                  : 710
ConfigString           : vmi307469.3key.local\\Demo MS Sub CA
Table                  : Request
Properties             : {[RequestID, 710], [Request.RequesterName, 3KEY\\nejaky.uzivatel], [CommonName, Users
                         Nějaký Uživatel], [NotBefore, 7/7/2023 9:25:52 AM]...}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_identified_certificates(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].certificate_template, "1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353"
                                                            ".10624234.204.2517003.8444064")
        self.assertEqual(templates[0].serial_number, "18000002c69a773092830df76a0000000002c6")
        self.assertEqual(templates[0].config_string, "vmi307469.3key.local\\Demo MS Sub CA")

    def test_parse_authority_data(self):
        data = """

Name                 : Demo MS Sub CA
DisplayName          : Demo MS Sub CA
ComputerName         : vmi307469.3key.local
ConfigString         : vmi307469.3key.local\\Demo MS Sub CA
DistinguishedName    : CN=Demo MS Sub CA,CN=Enrollment Services,CN=Public Key
                       Services,CN=Services,CN=Configuration,DC=3key,DC=local
Type                 : Enterprise Subordinate CA
IsEnterprise         : True
IsRoot               : False
OperatingSystem      : Microsoft Windows Server 2016 Datacenter
IsAccessible         : True
RegistryOnline       : True
ServiceStatus        : Running
SetupStatus          : ServerInstall, ClientInstall, SecurityUpgraded, ServerIsUptoDate
Certificate          : [Subject]
                         O=3Key Company s.r.o., CN=Demo MS Sub CA

                       [Issuer]
                         O=3Key Company s.r.o., CN=Demo Root CA

                       [Serial Number]
                         656879DC6DFCC35C431488317DDB331F486A3847

                       [Not Before]
                         10/13/2019 8:33:12 AM

                       [Not After]
                         10/9/2034 8:33:12 AM

                       [Thumbprint]
                         66829B517CB2169DCB015988DA72DE6B7A7D75DA

BaseCRL              :
DeltaCRL             :
EnrollmentServiceURI :
EnrollmentEndpoints  : {https://vmi307469.3key.local/Demo%20MS%20Sub%20CA_CES_Kerberos/service.svc/CES}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_authority_data(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].name, "Demo MS Sub CA")
        self.assertEqual(templates[0].display_name, "Demo MS Sub CA")
        self.assertEqual(templates[0].computer_name, "vmi307469.3key.local")
        self.assertEqual(templates[0].config_string, "vmi307469.3key.local\\Demo MS Sub CA")
        self.assertEqual(templates[0].ca_type, "Enterprise Subordinate CA")
        self.assertEqual(templates[0].is_enterprise, True)
        self.assertEqual(templates[0].is_root, False)
