import base64
from hashlib import sha256

from asn1crypto import cms, csr
from asn1crypto.algos import DigestAlgorithm, DigestAlgorithmId, SignedDigestAlgorithm
from asn1crypto.cms import ContentInfo, DigestAlgorithms, SignedData, SignerInfo, SignerInfos
from asn1crypto.core import OctetBitString, ParsableOctetString
from django.test import TestCase

from PyADCSConnector.utils.cmc import PKIData, TaggedCertificationRequest, TaggedRequest, TaggedRequests
from PyADCSConnector.utils.crmf import CertReqMsg, CertificationRequestNullSigned


class CmsTest(TestCase):
    def test_cms(self):
        crmff = "MIICXzCCAUMCAQEwggE8pRQwEjEQMA4GA1UEAwwHRXhhbXBsZaaCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAJoxEI0LamnXx2ouvcttJWuf5tAQxWhM4Heff2D5fWUEktg/jItDr20CZ5iWdXh+dGY2i9HrHxZFZYIDENWZRg3ue5F8UKHwoqfoJ1r1+9HP1k2i7FbECM6COW3hR0/P1qNUlxi/h5Vh6OmcI65Y3eo74SnnSEc2YLKkP2DI1E7Fs0qlgGamEK/9zAS/TLS5ukY20h09UGMpPhgi9VKpf6NetnKQwFNEI0klwGEuxNnlQEwshjE/qtD3hac5pQSNkIRobCnJtWlU6u6/XByRCt5A1UrCpiFySgjXjZuEKYBH5umCdYpDfo3td9SU8pD2YPpRJXqYAzx9F9/iBkHa+6ECAwEAAaGCARQwDQYJKoZIhvcNAQELBQADggEBACj+z6d+wjMroanC1XysAcpIPck1Na0mkz84SFna+QUS6MmL3/gzXB/EPRSuPhH43V3sfLDMEuo/yygCLSuVkS6ywD3jgNiFe5kNrm5jnbF1vDLBN7i5Wqm9eHibiM4974gU44uOSgKGJPllceCLRtQI7c37wP1mcimt/jmIc6Oo3SYNa+IIQcZV4IysMMB0T+Gum8+ZmvAb5spe3hAJ1UHckZ5kk7EKSqI4ucsJWD16xQq2in+H/CTWX1rxD213dyulebq1qpjjor9cFNSGicq5K9pt2PC2Hy+wJW/IDUIF08ccpODGC1tTZwRK65mVCt7lAP9P4Tfu7LMDdORkNwQ="
        crmf_CertReqMsg = CertReqMsg.load(base64.b64decode(crmff))

        pkcs10_new = CertificationRequestNullSigned()

        cri = csr.CertificationRequestInfo()
        cri['version'] = csr.Version(0)
        cri['subject'] = crmf_CertReqMsg['certReq']['certTemplate']['subject']
        cri['subject_pk_info'] = crmf_CertReqMsg['certReq']['certTemplate']['publicKey']

        pkcs10_new['certification_request_info'] = cri

        signature_algorithm = DigestAlgorithm()

        signature_algorithm['algorithm'] = DigestAlgorithmId('sha256')

        pkcs10_new['signature_algorithm'] = signature_algorithm

        pkcs10_new['signature'] = OctetBitString(sha256(cri.dump()).digest())

        print(base64.b64encode(pkcs10_new.dump()))

        content_info = ContentInfo()
        content_info['content_type'] = cms.ContentType.map('1.2.840.113549.1.7.2')

        signed_data = SignedData()
        signed_data['version'] = cms.CMSVersion(3)

        digest_algorithms = DigestAlgorithms()
        digest_algorithms.append(signature_algorithm)
        signed_data['digest_algorithms'] = digest_algorithms

        enc_ci = cms.EncapsulatedContentInfo()
        enc_ci['content_type'] = cms.ContentType.map('1.3.6.1.5.5.7.12.2')

        cmc_object = PKIData()
        tagged_csr = TaggedCertificationRequest()
        tagged_csr['bodyPartID'] = 1
        tagged_csr['certificationRequest'] = pkcs10_new
        tagged_request = TaggedRequest().load(tagged_csr.dump())

        tagged_requests = TaggedRequests()
        tagged_requests.append(tagged_request)
        cmc_object['reqSequence'] = tagged_requests

        print(base64.b64encode(cmc_object.dump()))

        # tagged_attributes = TaggedAttributes()
        # cmc_object['controlSequence'] = tagged_attributes

        enc_ci['content'] = ParsableOctetString(cmc_object.dump())
        signed_data['encap_content_info'] = enc_ci

        signer_info = SignerInfo()
        signer_info['version'] = cms.CMSVersion(3)
        signer_info['signature'] = base64.b64encode(pkcs10_new['signature'].dump())

        signer_info['sid'] = cms.SignerIdentifier({'subject_key_identifier': b'123456789'})
        signer_info['digest_algorithm'] = signature_algorithm

        signature_algorithm_si = SignedDigestAlgorithm()
        signature_algorithm_si['algorithm'] = '1.3.6.1.5.5.7.6.2'
        signature_algorithm_si['parameters'] = None

        signer_info['signature_algorithm'] = signature_algorithm_si

        signer_infos = SignerInfos()
        signer_infos.append(signer_info)
        signed_data['signer_infos'] = signer_infos

        content_info['content'] = signed_data

        print(base64.b64encode(content_info.dump()))
