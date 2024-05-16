import base64
from hashlib import sha256

from asn1crypto import cms, csr, x509
from asn1crypto.algos import DigestAlgorithm, DigestAlgorithmId, SignedDigestAlgorithm
from asn1crypto.cms import ContentInfo, DigestAlgorithms, SignedData, SignerInfo, SignerInfos, CertificateSet, \
    CMSAttributes, CMSAttribute
from asn1crypto.core import OctetBitString, ParsableOctetString, SequenceOf, OctetString, Null, ObjectIdentifier
from asn1crypto.csr import CRIAttributes, CRIAttribute, SetOfExtensions, CSRAttributeType
from asn1crypto.x509 import Extension, Extensions
from django.test import TestCase

from PyADCSConnector.utils.adcs_asn1 import CertificateTemplateOid
from PyADCSConnector.utils.cmc import PKIData, TaggedCertificationRequest, TaggedRequest, TaggedRequests, \
    TaggedAttributes, OtherMsgs, TaggedContentInfos
from PyADCSConnector.utils.cms_utils import create_cms
from PyADCSConnector.utils.crmf import CertReqMsg, CertificationRequestNullSigned
from PyADCSConnector.utils.dump_parser import TemplateData


class CmsTest(TestCase):

    def test_cms(self):
        cert = "MIIFGTCCAwGgAwIBAgIUZOuCdUKf964a1EzeyeGJlOktZgkwDQYJKoZIhvcNAQELBQAwQDEgMB4GA1UEAwwXRGVtb0NsaWVudFN1YkNBXzIzMDdSU0ExHDAaBgNVBAoMEzNLZXkgQ29tcGFueSBzLnIuby4wHhcNMjQwNDIyMDg1MDIwWhcNMjYwNDIyMDg1MDE5WjAVMRMwEQYDVQQDDAp0ZXN0bXN3Y2NlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApQSz+f7YqcWq5sN6q0S89VBR8kfDab3T9r4eu+NEikNuprphrqiuqCRMl64uEkyO6U9dTb+7ja7xOD6kdlhCSoMjhqPuAtOuGdUhQCC1aOEXBx3Rt42JhoOOTEQX7KexD2Gm/yXAvI332pUF7/AvVGnMsOJoZuJBwbTfL3kn/WHJrGoZBS3f4jW8lcaDXL5XbFvowEEW324MiAlxWaH2XbT5YflbBhz4qQFw8LoLmZeGmU3TupWE4LOfg5Xhx3U7Gwi0d2HS3LK+aXeAm5GO5sbTEGnHJe51gsSDPtjVFikRrQ5510ABF9FFv5s1wtD60HImhUO8x1Sc02JCL8CYFQIDAQABo4IBNDCCATAwDAYDVR0TAQH/BAIwADAfBgNVHSMEGDAWgBSVb1aJP6lv/cDXMMG3l1/mLEqvHTBYBggrBgEFBQcBAQRMMEowSAYIKwYBBQUHMAKGPGh0dHA6Ly9wa2kuM2tleS5jb21wYW55L2Nhcy9kZW1vL2RlbW9jbGllbnRzdWJjYV8yMzA3cnNhLmNydDARBgNVHSAECjAIMAYGBFUdIAAwEwYDVR0lBAwwCgYIKwYBBQUHAwIwTgYDVR0fBEcwRTBDoEGgP4Y9aHR0cDovL3BraS4za2V5LmNvbXBhbnkvY3Jscy9kZW1vL2RlbW9jbGllbnRzdWJjYV8yMzA3cnNhLmNybDAdBgNVHQ4EFgQUeMg+lJ0q1gFhCkyRM1pH3hKD05gwDgYDVR0PAQH/BAQDAgWgMA0GCSqGSIb3DQEBCwUAA4ICAQDKQ5bkzL7hjP7jghbV+GXpBnVmXcUIGEF1+SzThGk/w80Caq6xlRPz1UQ17MAty4FPgsz+kc93QFQnLUMIwmvqD0aWAkVNd6RRvY5mmTYE65c/DvkGNBCAWFdu8iDOXptnwBGdusV7bATodJQKbBX1uslgBma1a2YOrsIAvurPnTbN4BAAf5R7Gdk1RTpp129DbCFURwJP0aQPHkM/3GoXasf24HxKX9lX8HRPRQNp+BHfeT29+eGmSXGpqM4f6+j3XvgjeghaitnC257MqNX+cnX/BGDFy933QLTWS2yDbRMhYQ64llenz3kQ0h7RXzoNvyMwFJkMm7Pf3u4lEEzd2+cQTzxrozSevzASLxSHqP6cRbJD90rBbdqyII8OoOffNyTPzsd7DqoyVTbyQv7otKV/qRmbPvEnhAKuWYhxYwBsWIfkhoG8+q0AXPk1BQRGL1aYcfP1khqkpTmChmZmD7quqjPFsqoDM0xbHn22NaNNyMbj5OJQe3krpcJZMkgm/hMj0TRYUu2CD24VEVQ98abbsTKaYtjbgfgAUUcit+gxqcUzhT/aA71ZnkyxLkj4iVYeLN89jJYtTO/OEWUrgiK4O058hdzIk39rqpm317eAEgn9qVpsn6ksbezVWLYSQLLld0+b9Z3DLAd0R55iniZqUl/hAVG6w87tcs2IJQ=="
        issuerCert = "MIIGIzCCBAugAwIBAgIUXqFSYLp0ubziDvE6soPiV8juAyswDQYJKoZIhvcNAQELBQAwOzEbMBkGA1UEAwwSRGVtb1Jvb3RDQV8yMzA3UlNBMRwwGgYDVQQKDBMzS2V5IENvbXBhbnkgcy5yLm8uMB4XDTIzMDcxOTExMTQwMloXDTM4MDcxNTExMTQwMVowQDEgMB4GA1UEAwwXRGVtb0NsaWVudFN1YkNBXzIzMDdSU0ExHDAaBgNVBAoMEzNLZXkgQ29tcGFueSBzLnIuby4wggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDX4VT1wD0iNVPaojteRUZD5r2Dhtr9lmWggvFUcE9Pd8XAk7fQK0dI5Y1igPnyUazNqFTCHnI0UdGsHzBIY06urrUIW5VNUcRjXjX+kh86Y16LP8M0hvDl4oDK7EBW5a9gzJtsnFS71WxTurDrsJYgN3jJLBlmSi/yA8MaiY76fktI6++nB4O+uQfK7StpA9Dst+HLM6FLk7r39D/wIWfn2q/MCTF+h4OY+pEcJvNHk+1HHsuKOQOlYDeYGzN/CopK7Zmymu9DfgwpPcVXJ9dZBwx+G4dE3Ri0pnL/hfVaBEbNUkYDIgs5zRpb3ZN68JJy0XTmCcTAgiUZBYmiDhMSMBPl5mts40OpL5bewM+ekrAbFwNL4idUPS2V9XWOGy51UYtcjHUTQB9m9E+aP5ZfvDCZhu+yzenDcYT6UhENpgGfDpJ+im0jjNNgC+z58Y9uYRqN/w+HWrXermZxGQS6mkQ+iJLeEWWHDjFi4v0TjbHyhxPkQSAacJ4IWFT37eivVirQZFGuXpBEI51xvs25K24f0fxuLcAumS5APTPD90D2Xa5J1vMowsdtKgs5nZP3dKmmSr2reAsiodNtBroUpWcjznurHf43zhAlQuQvCCn12zyaXGtaF/Cl0Aj0nmuVf6fEhoCM4xiECqlmtoXKTTA7vaMRTGgXlR1iyHKaXwIDAQABo4IBGDCCARQwDwYDVR0TAQH/BAUwAwEB/zAfBgNVHSMEGDAWgBQkykIO76rGkT7RqvoTWHgqFlBGiTBTBggrBgEFBQcBAQRHMEUwQwYIKwYBBQUHMAKGN2h0dHA6Ly9wa2kuM2tleS5jb21wYW55L2Nhcy9kZW1vL2RlbW9yb290Y2FfMjMwN3JzYS5jcnQwEQYDVR0gBAowCDAGBgRVHSAAMEkGA1UdHwRCMEAwPqA8oDqGOGh0dHA6Ly9wa2kuM2tleS5jb21wYW55L2NybHMvZGVtby9kZW1vcm9vdGNhXzIzMDdyc2EuY3JsMB0GA1UdDgQWBBSVb1aJP6lv/cDXMMG3l1/mLEqvHTAOBgNVHQ8BAf8EBAMCAYYwDQYJKoZIhvcNAQELBQADggIBAGDcHP44ZO26c5p6XyMOzuc7TMkMeDdnqcPD8y+Cnj4V/r8Qq8gdpzjdozw3NMtVfnHP72P1XOcG5U3NUaRtEnP0C4SHnciPttV1WWkaQhzLNU6nnR1M7OiqHVkAmHHZ0U1R8ih8h4LvHO/UzcXFA5avn23udOfZL9tSN9/ljyLIdPAievFGGv94JB+YlykkUHzlrrlFADct4CVKiwoMjhdBMoLnFetNr6ZmTXbImnLMjVhhZHQ0cQfFdTnS7KeN2O4orSqiptkPAZ7ySsP4jEzTVxGzOZbsVna4XeGr5m2P6+ONVIj801Zp5QZh1F7IYV6M2jnIzXcE4+xrn1Nwj0SkOY4NUK5Gh16y78f/R+igjIC+L3VCs9Pr4ePepx1wJSb+180Gy0FED/4DQyAX0bAyGRv6POVsaIpRLAGWkkh6Qn4g9lAVLZydmXAJuQ05m0X4Ljq9EshPwad9tcVGIFcGvw7Wat+75ib40CarKP8OGp//cDVSqlv4JRPNwgo/0lhTXQP2tNNODOMGn3qtPy9MYHHyUjsnhbiDtUGQHL7QrZIAB00aTJFwD4YcMqjTd0b0Sdi34kPrhYLvY5ouBREsF50DhrUrz45YKbZiB5kWA8NsGgbLGiJQurxuNFwezwDYziAyWn+Xr01o8dLTEo5FZOEhWhKbEp4GGoq9BD8v"
        crmf_encoded = "MIICXzCCAUMCAQEwggE8pRQwEjEQMA4GA1UEAwwHRXhhbXBsZaaCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJoxEI0LamnXx2ouvcttJWuf5tAQxWhM4Heff2D5fWUEktg/jItDr20CZ5iWdXh+dGY2i9HrHxZFZYIDENWZRg3ue5F8UKHwoqfoJ1r1+9HP1k2i7FbECM6COW3hR0/P1qNUlxi/h5Vh6OmcI65Y3eo74SnnSEc2YLKkP2DI1E7Fs0qlgGamEK/9zAS/TLS5ukY20h09UGMpPhgi9VKpf6NetnKQwFNEI0klwGEuxNnlQEwshjE/qtD3hac5pQSNkIRobCnJtWlU6u6/XByRCt5A1UrCpiFySgjXjZuEKYBH5umCdYpDfo3td9SU8pD2YPpRJXqYAzx9F9/iBkHa+6ECAwEAAaGCARQwDQYJKoZIhvcNAQELBQADggEBACj+z6d+wjMroanC1XysAcpIPck1Na0mkz84SFna+QUS6MmL3/gzXB/EPRSuPhH43V3sfLDMEuo/yygCLSuVkS6ywD3jgNiFe5kNrm5jnbF1vDLBN7i5Wqm9eHibiM4974gU44uOSgKGJPllceCLRtQI7c37wP1mcimt/jmIc6Oo3SYNa+IIQcZV4IysMMB0T+Gum8+ZmvAb5spe3hAJ1UHckZ5kk7EKSqI4ucsJWD16xQq2in+H/CTWX1rxD213dyulebq1qpjjor9cFNSGicq5K9pt2PC2Hy+wJW/IDUIF08ccpODGC1tTZwRK65mVCt7lAP9P4Tfu7LMDdORkNwQ="
        crmf_CertReqMsg = CertReqMsg.load(base64.b64decode(crmf_encoded))

        # -----------------------------------------------------------
        # create PKCS#10 request with Null Signature
        # -----------------------------------------------------------
        pkcs10_new = CertificationRequestNullSigned()

        cri = csr.CertificationRequestInfo()
        cri['version'] = csr.Version(0)
        cri['subject'] = crmf_CertReqMsg['certReq']['certTemplate']['subject']
        cri['subject_pk_info'] = crmf_CertReqMsg['certReq']['certTemplate']['publicKey']

        cri_attributes = CRIAttributes()
        extension_cri_attr = CRIAttribute()
        extension_cri_attr['type'] = CSRAttributeType('extension_request')

        # -----------------------------------------------------------
        # attributes for certificate template v1
        # -----------------------------------------------------------
        # extension = Extension()
        # extension['extn_id'] = 'microsoft_enroll_certtype'
        # extension['extn_value'] = 'Administrator'

        # -----------------------------------------------------------
        # attributes for certificate template v2,3,4
        # -----------------------------------------------------------
        template_v2 = Extension()
        template_v2['extn_id'] = '1.3.6.1.4.1.311.21.7'

        cert_template_oid = CertificateTemplateOid()
        cert_template_oid['templateID'] = ObjectIdentifier('1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.4506045.4701483')
        cert_template_oid['templateMajorVersion'] = 100
        cert_template_oid['templateMinorVersion'] = 3

        template_v2['extn_value'] = cert_template_oid.dump()

        extensions = Extensions()
        # extensions.append(extension)
        extensions.append(template_v2)
        extensions_set = SetOfExtensions()
        extensions_set.append(extensions)
        extension_cri_attr['values'] = extensions_set

        cri_attributes.append(extension_cri_attr)

        cri['attributes'] = cri_attributes

        # create challenge_password attribute
        # cri_attribute = CRIAttribute()
        # cri_attribute['type'] = 'challenge_password'
        # challenge_password = SetOfDirectoryString()
        # challenge_password.append(UTF8String('123456789'))
        # cri_attribute['values'] = challenge_password
        # cri_attributes = CRIAttributes()
        # cri_attributes.append(cri_attribute)
        # cri['attributes'] = cri_attributes

        signature_algorithm = DigestAlgorithm()
        signature_algorithm['algorithm'] = DigestAlgorithmId('sha256')
        signature_algorithm['parameters'] = None

        signature_algorithm_null = DigestAlgorithm()
        signature_algorithm_null['algorithm'] = DigestAlgorithmId('sha256')
        signature_algorithm_null['parameters'] = Null()

        pkcs10_new['certification_request_info'] = cri
        pkcs10_new['signature_algorithm'] = signature_algorithm_null
        pkcs10_new['signature'] = OctetBitString(sha256(cri.dump()).digest())

        print(base64.b64encode(pkcs10_new.dump()))

        # -----------------------------------------------------------
        # create PKI Data
        # input: PKCS#10 request with Null Signature
        # -----------------------------------------------------------
        cmc_object = PKIData()

        tagged_csr = TaggedCertificationRequest()
        tagged_csr['bodyPartID'] = 0
        tagged_csr['certificationRequest'] = pkcs10_new

        # tagged_request = TaggedRequest().load(tagged_csr.dump())

        tagged_request = TaggedRequest({'tcr': tagged_csr})

        tagged_requests = TaggedRequests()
        tagged_requests.append(tagged_request)

        tagged_attributes = TaggedAttributes(SequenceOf())

        tagged_content_infos = TaggedContentInfos(SequenceOf())

        other_msgs = OtherMsgs(SequenceOf())

        cmc_object['controlSequence'] = tagged_attributes
        cmc_object['reqSequence'] = tagged_requests
        cmc_object['cmsSequence'] = tagged_content_infos
        cmc_object['otherMsgSequence'] = other_msgs

        print(base64.b64encode(cmc_object.dump()))

        # -----------------------------------------------------------
        # create CMS signed data
        # input: PKI Data
        # -----------------------------------------------------------
        digest_algorithms = DigestAlgorithms()
        digest_algorithms.append(signature_algorithm)

        enc_ci = cms.EncapsulatedContentInfo()
        enc_ci['content_type'] = cms.ContentType.map('1.3.6.1.5.5.7.12.2')
        enc_ci['content'] = ParsableOctetString(cmc_object.dump())

        signature_algorithm_si = SignedDigestAlgorithm()
        signature_algorithm_si['algorithm'] = '1.3.6.1.5.5.7.6.2'
        signature_algorithm_si['parameters'] = Null()

        issuer_certificate = x509.Certificate.load(base64.b64decode(issuerCert))
        certificate = x509.Certificate.load(base64.b64decode(cert))

        signed_attributes = CMSAttributes()
        attribute_content_type = CMSAttribute()
        attribute_content_type['type'] = '1.2.840.113549.1.9.3'  # PKCS#9 content type
        attribute_content_type['values'] = ['1.3.6.1.5.5.7.12.2']

        attribute_message_digest = CMSAttribute()
        attribute_message_digest['type'] = '1.2.840.113549.1.9.4'  # message digest
        # attribute_message_digest['values'] = [sha256(enc_ci['content'].dump()).digest()]
        attribute_message_digest['values'] = [OctetString(sha256(enc_ci['content'].native).digest())]

        signed_attributes.append(attribute_content_type)
        signed_attributes.append(attribute_message_digest)

        signer_info = SignerInfo()
        signer_info['version'] = cms.CMSVersion(1)  # because the sid is issuer_and_serial_number
        # signer_info['sid'] = cms.SignerIdentifier({'subject_key_identifier': b'123456789'})
        signer_info['sid'] = cms.SignerIdentifier(
            {'issuer_and_serial_number': {
                'issuer': issuer_certificate['tbs_certificate']['subject'],
                'serial_number': certificate['tbs_certificate']['serial_number']}})
        signer_info['digest_algorithm'] = signature_algorithm
        signer_info['signed_attrs'] = signed_attributes
        signer_info['signature_algorithm'] = signature_algorithm_si
        signer_info['signature'] = OctetString(sha256(signed_attributes.dump()).digest())

        signer_infos = SignerInfos()
        signer_infos.append(signer_info)

        certificates = CertificateSet()
        certificates.append(certificate)

        signed_data = SignedData()
        signed_data['version'] = cms.CMSVersion(3)
        signed_data['digest_algorithms'] = digest_algorithms
        signed_data['encap_content_info'] = enc_ci
        # signed_data['certificates'] = certificates
        signed_data['signer_infos'] = signer_infos

        content_info = ContentInfo()
        content_info['content_type'] = cms.ContentType.map('1.2.840.113549.1.7.2')
        content_info['content'] = signed_data

        print(base64.b64encode(content_info.dump()))

    def test_cms_util(self):
        crmf_encoded = "MIICXzCCAUMCAQEwggE8pRQwEjEQMA4GA1UEAwwHRXhhbXBsZaaCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJoxEI0LamnXx2ouvcttJWuf5tAQxWhM4Heff2D5fWUEktg/jItDr20CZ5iWdXh+dGY2i9HrHxZFZYIDENWZRg3ue5F8UKHwoqfoJ1r1+9HP1k2i7FbECM6COW3hR0/P1qNUlxi/h5Vh6OmcI65Y3eo74SnnSEc2YLKkP2DI1E7Fs0qlgGamEK/9zAS/TLS5ukY20h09UGMpPhgi9VKpf6NetnKQwFNEI0klwGEuxNnlQEwshjE/qtD3hac5pQSNkIRobCnJtWlU6u6/XByRCt5A1UrCpiFySgjXjZuEKYBH5umCdYpDfo3td9SU8pD2YPpRJXqYAzx9F9/iBkHa+6ECAwEAAaGCARQwDQYJKoZIhvcNAQELBQADggEBACj+z6d+wjMroanC1XysAcpIPck1Na0mkz84SFna+QUS6MmL3/gzXB/EPRSuPhH43V3sfLDMEuo/yygCLSuVkS6ywD3jgNiFe5kNrm5jnbF1vDLBN7i5Wqm9eHibiM4974gU44uOSgKGJPllceCLRtQI7c37wP1mcimt/jmIc6Oo3SYNa+IIQcZV4IysMMB0T+Gum8+ZmvAb5spe3hAJ1UHckZ5kk7EKSqI4ucsJWD16xQq2in+H/CTWX1rxD213dyulebq1qpjjor9cFNSGicq5K9pt2PC2Hy+wJW/IDUIF08ccpODGC1tTZwRK65mVCt7lAP9P4Tfu7LMDdORkNwQ="
        ca_name = 'Authority'
        template_v1 = TemplateData('temp_1', 'temp_displ', 1, 1, '1.2.3')
        create_cms(crmf_encoded, ca_name, template_v1)
        template_v2 = TemplateData('temp_1', 'temp_displ', 1, 2, '1.2.3')
        create_cms(crmf_encoded, ca_name, template_v2)


