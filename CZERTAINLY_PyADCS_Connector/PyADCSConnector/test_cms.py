import base64

from asn1crypto.cms import ContentInfo
from django.test import TestCase

from PyADCSConnector.utils.adcs_asn1 import CertificateTemplateOid
from PyADCSConnector.utils.cmc import PKIData
from PyADCSConnector.utils.cms_utils import create_cms
from PyADCSConnector.utils.dump_parser import TemplateData


class CmsTest(TestCase):

    def test_cms_util(self):
        crmf_encoded = "MIIDHTCCAxkwggH9AgEAMIIB9qNmMGQxDzANBgNVBAoMBnRvY2VjejEmMCQGA1UEAwwdZGV2ZWxvcC5sb2NhbGhvc3QubG9jYWxkb21haW4xKTAnBgkqhkiG9w0BCQEWGnJvb3RAbG9jYWxob3N0LmxvY2FsZG9tYWlupWYwZDEPMA0GA1UECgwGdG9jZWN6MSYwJAYDVQQDDB1kZXZlbG9wLmxvY2FsaG9zdC5sb2NhbGRvbWFpbjEpMCcGCSqGSIb3DQEJARYacm9vdEBsb2NhbGhvc3QubG9jYWxkb21haW6mggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDIrii/N6zI35rtw6sYmApohhNqOXRa8ktsqDPROdzdNc55aBVyTQFvf0z1XRi26l4GhsUv3KpLVTLV3vrCXtOTAeZccQgNqfKqDIVByjzWxGxFMuiTwpToB+a/CqXblaavTlyrv9varnxBEDjXK7H5iA4U+HxhM+WWidcSstnqGG8CnTmWS9cnj163zF01JzQANuIXKQ1CvJkHaMidbj5n5+w/nU/73BZEhnKivbOw3WWgVlV7fnR325FCF25J4AzJ2YyXo0Xu95cH0psjX0DM/ZroV+geiPZgGUp8cszkNYJMg5vHXSIQnYDDhDyiACy0QUqpxmK2iZdAqpTeI2W7AgMBAAGhggEUMA0GCSqGSIb3DQEBCwUAA4IBAQAeIxAUbjTOqCwl1egb7+Sr2U9kA65+tgydM5zYmc1qcOBFAo+ngMAD8WaG3hJRZgjGQP/HYxmx7lJAYU6RwvgD+c0bOHuB7kawFL1oyv0zhOVUnKmLrERVTjq1PYNYaEt3dfsrhGy1aziyyH4K4nOmBwINzJmy0wuPI8MeCbBTlu4V3hdmo8OpruCHxN2CgsxyrMwcPLUXQFy3lMhx3Mfc3ht7u8eFcaKLbraxmDDwtZbtoEcBTZFFrKoFkJERXZGiVRNkuk/vIc/ZpRvwg1y5CvbPCgj3CRbwrwOfXSWRYG7R7SJDMJTfOlAPt7GksF/kQr7aakQcsf9wBQ4K1HjE"
        ca_name = 'Authority'
        template_v1 = TemplateData('WebServer', 'temp_displ', '1', '1', '1.2.3')
        cms_v1 = create_cms(crmf_encoded, ca_name, template_v1)
        cms_object = ContentInfo.load(base64.b64decode(cms_v1))
        pki_data = PKIData.load(cms_object['content']['encap_content_info']['content'].native)
        cert_request = pki_data['reqSequence'][0].chosen['certificationRequest']

        print(cms_v1)

        # Check if hash value of the Certificate Request Info has expected value
        self.assertEqual(base64.b64encode(cert_request['signature'].native), b'AOlSQLNom8Jl3L0MxuBZgvcHYBhj7zHIr5A36kudDI4=')

        # Check if Certificate Template extension has correct value
        extension = cert_request['certification_request_info']['attributes'][0]['values'][0][0]
        self.assertEqual(extension['extn_value'].native, template_v1.name)

        # Check if Signer Info has correctly set SID issuer name
        signer_info = cms_object['content']['signer_infos'][0]
        self.assertEqual(signer_info['sid'].chosen['issuer'].native['common_name'], ca_name)

        # Check if Signer Info has expected signature value of Encapsulated Content Info content
        self.assertEqual(base64.b64encode(signer_info['signature'].native), b'+jCEBGh5z8VMhdb0yTX+AjFUuwE7YCh7YxkDE6Wze2M=')

        template_v2 = TemplateData('WebServer', 'temp_displ', '2', '2.4', '1.2.3')

        cms_v2 = create_cms(crmf_encoded, ca_name, template_v2)

        # Check if Certificate Template OID has been set correctly
        cms_object = ContentInfo.load(base64.b64decode(cms_v2))
        pki_data = PKIData.load(cms_object['content']['encap_content_info']['content'].native)
        cert_request = pki_data['reqSequence'][0].chosen['certificationRequest']
        extension = cert_request['certification_request_info']['attributes'][0]['values'][0][0]
        cert_template_oid = CertificateTemplateOid.load(extension['extn_value'].native)
        self.assertEqual(cert_template_oid['templateID'].native, template_v2.oid)
        self.assertEqual(str(cert_template_oid['templateMajorVersion'].native), template_v2.version.split('.')[0])
        self.assertEqual(str(cert_template_oid['templateMinorVersion'].native), template_v2.version.split('.')[1])






