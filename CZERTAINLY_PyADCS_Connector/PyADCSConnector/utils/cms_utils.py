import base64
from hashlib import sha256

from asn1crypto import csr
from asn1crypto.algos import DigestAlgorithm, DigestAlgorithmId
from asn1crypto.core import OctetBitString

from PyADCSConnector.utils.crmf import CertificationRequestNullSigned, CertReqMsg


def convert_crmf_to_null_signed_pkcs10(encoded):
    cert_req_msq = CertReqMsg.load(base64.b64decode(encoded))
    pkcs10 = CertificationRequestNullSigned()
    cert_template = cert_req_msq['certReq']['certTemplate']

    cri = csr.CertificationRequestInfo()
    cri['version'] = csr.Version(0)
    cri['subject'] = cert_template['certReq']['certTemplate']['subject']
    cri['subject_pk_info'] = cert_req_msq['certReq']['certTemplate']['publicKey']
    pkcs10['certification_request_info'] = cri

    signature_algorithm = DigestAlgorithm()
    signature_algorithm['algorithm'] = DigestAlgorithmId('sha256')
    pkcs10['signature_algorithm'] = signature_algorithm

    pkcs10['signature'] = OctetBitString(sha256(cri.dump()).digest())

    return pkcs10
