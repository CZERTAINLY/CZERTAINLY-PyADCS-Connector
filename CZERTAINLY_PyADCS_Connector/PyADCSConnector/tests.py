import winrm
from django.test import TestCase

from PyADCSConnector.utils.dump_parser import DumpParser


class DumpParserTest(TestCase):
    def test_parse_certificates(self):
        data = """

RequestID                  : 787
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\VMI307469$
Request.SubmittedWhen      : 12/28/2023 12:26:31 PM
Request.CommonName         : lab02.3key.company
CertificateTemplate        : WebServer
RawCertificate             : MIIFNjCCAx6gAwIBAgITGAAAAxP9YXII0BMNqQAAAAADEzANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzEyMjgxMjE2MzFaFw0yNTEyMjcxMjE2MzFaMB0xGzAZ
                             BgNVBAMTEmxhYjAyLjNrZXkuY29tcGFueTCCASIwDQYJKoZIhvcNAQEBBQADggEP
                             ADCCAQoCggEBAK5b2H5I8iJOYNxWSRah3rDUz9BPjADu2OjvlNhqJqJ3vFNyPlms
                             GHmtWb1SvQAjZGRdIF+hC1YSchs/u4mq5XxBMCjI6b9Ne2o8slkDobDaHhwAJCRt
                             9RuVr+goVIM+WovNEexlgK/7fScV9Nej0+pzu0tT1vIwiZU81O12ebg3Lg7LaLsM
                             91Vefhs8Tc+tF8hfnvZ2ywWCEvx0kQD8OP6bjhoVOe/hgx9bhksI0aJg7db1dbLC
                             sbr/z6vOEj3E7jH1zxNQ6iPQ3sPvaf/+kCHOSoJjpImkQiq0evYCdeSR/NNTc+Hq
                             b3tcYVIBhQI2dgbj1c9xe4omyp7F3XJZdj0CAwEAAaOCAVMwggFPMCEGCSsGAQQB
                             gjcUAgQUHhIAVwBlAGIAUwBlAHIAdgBlAHIwEwYDVR0lBAwwCgYIKwYBBQUHAwEw
                             DgYDVR0PAQH/BAQDAgWgMB0GA1UdDgQWBBTcDLXCwo8HCKLOPY2JKoDIzgjZ7zAd
                             BgNVHREEFjAUghJsYWIwMi4za2V5LmNvbXBhbnkwHwYDVR0jBBgwFoAUksK831XF
                             wZOFSQf3rMkdC2gBB1EwTQYDVR0fBEYwRDBCoECgPoY8aHR0cDovL2xhYjAyLjNr
                             ZXkuY29tcGFueS9jcmxzL2RlbW8vRGVtbyUyME1TJTIwU3ViJTIwQ0EuY3JsMFcG
                             CCsGAQUFBwEBBEswSTBHBggrBgEFBQcwAYY7aHR0cDovL2xhYjAyLjNrZXkuY29t
                             cGFueS9jYXMvZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBDQS5jcnQwDQYJKoZIhvcN
                             AQENBQADggIBALAVZ8r9Z6lDmiui3FhD3RdfghLENLUB+SBbDtDNg/+udKFLdU7l
                             eaew2pPi/SoPFZOMKAW5lC5Iq0MXCeppTe/gvE6Q8+doJ6RqEQwtpSYkG3zZjnEX
                             qYoeWBu0QFIYueuYlvPret3t8whTZt32wCDPyOp6ks1jDa2WMRKge+1xs4bBUFBn
                             wMqlifBUf9ulNlaVTW0Y32zluqlGiKnbrHSveJ3TBUbG7sbqhQ6XB1AfZIwCK5JQ
                             yLI3WAnNr1ziFlvERZzYrYDHviBYtdOZgp+ttmeT3XddrMXliklRGQ5Rl9O8EL5T
                             Dg9ViXM3PH04g6Ce84oJXevy7Ohxdok7JvdKA74fsfbRYM6ZP5AftXt3apmF0GoO
                             gbU7Y9z9q+7w++BX0e61cNdmHGOpxZa7OKLGhNel86lVgPeggY+PdYyfp+18v3je
                             /0z5vHR3pmcBqbrYP0JZj/XHVYNyXTf6ba2I/xiABTux/ntQIVbKHZTT/oVwuYa6
                             ISCJ9GKFKoB1u3MmDx2zAHESaTJmrAQZc259cCnUuboR37L83v00Px6MfAmo8yfX
                             n65WTcqigQBOfWCOlJsRKS+q56+zRTotSxTaBQbnsloCS8Xw9x9pHfWRk5x6A5ew
                             k+c+s1LmTHr6WQF7NlwiG1rQ859i2hw7Fnlxd/2ro25EfD79Q55ZOU6H
                             
CertificateTemplateOid     : WebServer
RowId                      : 787
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 787], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], 
                             [Request.RequesterName, 3KEY\\VMI307469$]...}
RequestID                  : 788
Request.StatusCode         : 0
Request.DispositionMessage : Revoked by 3KEY\\nejaky.uzivatel
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 12/30/2023 2:17:34 PM
Request.CommonName         : signserver-ra-01
CertificateTemplate        : WebServer
RawCertificate             : MIIFFTCCAv2gAwIBAgITGAAAAxSPMU0RrjbifAAAAAADFDANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzEyMzAxNDA3MzRaFw0yNTEyMjkxNDA3MzRaMBsxGTAX
                             BgNVBAMTEHNpZ25zZXJ2ZXItcmEtMDEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
                             ggEKAoIBAQCgyWCtOYPVN45+tIyWg1bkTtVHew5dtAV6cJkHnfTYFo0MFMIs0US1
                             DnSZmMZUaUL73Ic6M9YDmsSdjEh4BiwJIBmKSy6lkg0lxOEzqYmu0K0YEBm3JjMY
                             l/fkPl+bre28xY5a9U5f1l3BVufxdR1+h7dlnSyaDMp2b8CqD3icr+4LO2HzOpwS
                             FlrMPuPf+uM58G2GeQsnePjxyDaRfIO58v064AcqB8OPLBq34J4D15RsGz5HtS9Y
                             RWSrzy0HFt3ipHzcaUucLnVTBeYpZKBl64+k4LAYINNq8hsb9TbVdvu8f3d1fXdB
                             32DJduOfnUBPB/Hz3sktPd/77i67FUoPAgMBAAGjggE0MIIBMDAdBgNVHQ4EFgQU
                             +/jrrO9jvD3ecJdurHKYa83v/MYwHwYDVR0jBBgwFoAUksK831XFwZOFSQf3rMkd
                             C2gBB1EwTQYDVR0fBEYwRDBCoECgPoY8aHR0cDovL2xhYjAyLjNrZXkuY29tcGFu
                             eS9jcmxzL2RlbW8vRGVtbyUyME1TJTIwU3ViJTIwQ0EuY3JsMFcGCCsGAQUFBwEB
                             BEswSTBHBggrBgEFBQcwAYY7aHR0cDovL2xhYjAyLjNrZXkuY29tcGFueS9jYXMv
                             ZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBDQS5jcnQwIQYJKwYBBAGCNxQCBBQeEgBX
                             AGUAYgBTAGUAcgB2AGUAcjAOBgNVHQ8BAf8EBAMCBaAwEwYDVR0lBAwwCgYIKwYB
                             BQUHAwEwDQYJKoZIhvcNAQENBQADggIBAMS6CoozrYDB0EBstl7lJiCK4ki6Ixpl
                             HCJZCQRatyMvUu48/cTDwPz+nNsDFuO691+6R3f0RJ5gsvtLyP0l+/h0IuK7DMOa
                             Tx8/k8xaHh5LXGcmkr5JREXgCqq35kImWfprsNEZ7HBDT24WmTedhy3L61igwlOY
                             82f1IA3ZAZ/jyoOnRV0mo1xmzyvUQ0WWlprGFeeE5YymaZeCWpLDdhrwOPP9iFcf
                             pNXc+mlPdG4NXUA+BKzZ0pM0J7VnSr9Vbnk6iSzAQFCEQFDee7v7gJr6tzpmoSWR
                             QUghA0cVlKg9ETx0jor+Uv6nJqPW/nusfn7Nx0sX/Ieh+At6OXa5wXJ09Y6GAz64
                             qudqBskp5mMtxFocmG6nHseo9wA3W8bQaoJYW+yyOqQhRGd1BuCsLYLR/M1n76of
                             ANSC3ZRkWdImsGZbqrCB5CcjOG9VTbVkO+O1kCp9uu0AALp+87firfOG7ggVWWkx
                             sCL0PuR/QuWlXsXSh2qFx/2MF/834tCRozbAOlBhY3WAzesvsBpZtEI/nkZSWe7a
                             kDY6gmYk71kjmKqxrw8CIzDVa+pWe6/TuMuwnVUttLOLsu7rSY26pBte8sMtf+Gn
                             yXmIwqYWDUtjhA7tjE1gtVK19z3MKUQg0zPTcphikOcxps+nVrUNvzCS6/Mnu88l
                             yR3kZc7dtNpz
                             
CertificateTemplateOid     : WebServer
RowId                      : 788
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 788], [Request.StatusCode, 0], [Request.DispositionMessage, Revoked by 
                             3KEY\\nejaky.uzivatel], [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}
RequestID                  : 789
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 12/31/2023 9:33:55 AM
Request.CommonName         : testpy
CertificateTemplate        : WebServer
RawCertificate             : MIIEhzCCAm+gAwIBAgITGAAAAxVSi91EVbaymgAAAAADFTANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzEyMzEwOTIzNTVaFw0yNTEyMzAwOTIzNTVaMBExDzAN
                             BgNVBAMTBnRlc3RweTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAtKU1kDjC
                             x9U8bN+YY6CKI9mkxd1K7Z7K6gbcyIJ1pC+M53ONRe59p2JD9zfgJRbkQTilzffO
                             hfmFebEMq0Lt0OJdP1TOD9BtlA3Sc0QVKya46JfpEY8oYHq05JDV/kMQWaJPiDhk
                             6/m6hzQx8egKcv/8G4dvHBcDOfuY28cldAECAwEAAaOCATQwggEwMB0GA1UdDgQW
                             BBQKmJn706mQCPOnGyC6I/oHUMBf5jAfBgNVHSMEGDAWgBSSwrzfVcXBk4VJB/es
                             yR0LaAEHUTBNBgNVHR8ERjBEMEKgQKA+hjxodHRwOi8vbGFiMDIuM2tleS5jb21w
                             YW55L2NybHMvZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBDQS5jcmwwVwYIKwYBBQUH
                             AQEESzBJMEcGCCsGAQUFBzABhjtodHRwOi8vbGFiMDIuM2tleS5jb21wYW55L2Nh
                             cy9kZW1vL0RlbW8lMjBNUyUyMFN1YiUyMENBLmNydDAhBgkrBgEEAYI3FAIEFB4S
                             AFcAZQBiAFMAZQByAHYAZQByMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggr
                             BgEFBQcDATANBgkqhkiG9w0BAQ0FAAOCAgEAmXVJl3otyFcoUrr/UhjBJXmpg+iv
                             tRLhDKPoVSKbMCSY2tBSGeQ9V3kE5+KQI+om1plTXKQBgHaFOGamq3K1DytjEJuK
                             TkwmWU4QVmkCYwv1qYEMQ5gqGWU1BDhuS43Q5oTR7Hv2G/dGxGaZDNycXE5aT/7T
                             X7KJlIL5bC63i0ng2NVjhgqmHLRP48K0T8e3sX0jRRDKbpAVY04VBOv4WSr6M7sn
                             Ib626eXEs96JgKnRp6wIJRwvbaBJdfJZpFBmBwTBzPjmNt+29+IDYHt3rQOA46Dg
                             SEKTOwptKgZzXHig1kVtM/8eebyIV8wls5HwOfQ2VTc/uPjrouD9SAW76wQLjvZd
                             14py+SafebFvEch//4QJhrPqYV5i7X3naFEIbtosDCvocT3eqq2FgWQAKzg84UJR
                             3bo6n5mWXIDoWwxdTdrbzxmYkPbIZpiGJhtHIbYJpxZHrbH7pma43Rtoo2PPXnl6
                             ORaTIFdYcOmff11foa/8QbyzgNSzDlxeUcbKaS/vjiPgY+/QPsc7KUVTVbrd3jIB
                             sc8BgWEMXzIEqBGZixNnJrpavZW9u9E2AhhztUjGd84Ok77bUeCgE620NyKrIZOx
                             F4D6SjYGvPiXdWEkVWKVYO6ego/GSYEzzFqwKWnp+EDnaj+8Vjc3LYD01WtPucDz
                             BkciW85+HYbHuwE=
                             
CertificateTemplateOid     : WebServer
RowId                      : 789
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 789], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], 
                             [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_certificates(result)
        self.assertEqual(len(templates), 3)
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

RequestID                  : 810
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 1/8/2024 4:56:32 PM
Request.CommonName         : signserver-ra-01
CertificateTemplate        : WebServer
SerialNumber               : 180000032a9a1aac7197589cef00000000032a
CertificateTemplateOid     : WebServer
RowId                      : 810
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 810], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], 
                             [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_identified_certificates(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].certificate_template, "WebServer")
        self.assertEqual(templates[0].serial_number, "180000032a9a1aac7197589cef00000000032a")
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
