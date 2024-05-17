import base64
from hashlib import sha256

from asn1crypto.algos import DigestAlgorithm, DigestAlgorithmId, SignedDigestAlgorithm
from asn1crypto.cms import ContentInfo, ContentType, SignedData, CMSVersion, DigestAlgorithms, \
    EncapsulatedContentInfo, SignerInfos, SignerInfo, CMSAttributes, CMSAttribute, IssuerAndSerialNumber
from asn1crypto.core import OctetBitString, SequenceOf, ObjectIdentifier, ParsableOctetString, OctetString, Null
from asn1crypto.csr import SetOfExtensions, CRIAttributes, CRIAttribute, CSRAttributeType, CertificationRequestInfo, \
    Version
from asn1crypto.x509 import Extension, Extensions, Name

from PyADCSConnector.utils.adcs_asn1 import CertificateTemplateOid
from PyADCSConnector.utils.cmc import PKIData, TaggedCertificationRequest, TaggedRequest, TaggedRequests, \
    TaggedAttributes, TaggedContentInfos, OtherMsgs
from PyADCSConnector.utils.crmf import CertificationRequestNullSigned, CertReqMessages
from PyADCSConnector.utils.dump_parser import TemplateData


def create_cms(crmf, ca_name, template: TemplateData):
    pkcs10 = convert_crmf_to_null_signed_pkcs10(crmf, template)
    pki_data = create_pki_data(pkcs10)
    content_info = ContentInfo()
    content_info['content_type'] = ContentType.map('1.2.840.113549.1.7.2')
    content_info['content'] = create_signed_data(pki_data, ca_name)

    return base64.b64encode(content_info.dump())


def convert_crmf_to_null_signed_pkcs10(encoded, template: TemplateData):
    cert_req_msq = CertReqMessages.load(base64.b64decode(encoded))[0]
    # Create CRI
    cri = CertificationRequestInfo()
    cri['version'] = Version(0)
    cri['subject'] = cert_req_msq['certReq']['certTemplate']['subject']
    cri['subject_pk_info'] = cert_req_msq['certReq']['certTemplate']['publicKey']

    # Create Extension Request Based on Certificate Template
    extension = Extension()

    if template.schema_version == '1':
        extension['extn_id'] = 'microsoft_enroll_certtype'
        extension['extn_value'] = template.name
    else:
        extension['extn_id'] = '1.3.6.1.4.1.311.21.7'
        # Create Certificate Template OID
        cert_template_oid = CertificateTemplateOid()
        cert_template_oid['templateID'] = ObjectIdentifier(template.oid)
        # Schema version - major.minor
        versions = template.version.split('.')
        cert_template_oid['templateMajorVersion'] = int(versions[0])
        cert_template_oid['templateMinorVersion'] = int(versions[1])
        extension['extn_value'] = cert_template_oid.dump()

    extensions = Extensions()
    extensions.append(extension)

    extensions_set = SetOfExtensions()
    extensions_set.append(extensions)

    # Create CRI Attribute from Extension

    cri_attributes = CRIAttributes()
    extension_cri_attr = CRIAttribute()
    extension_cri_attr['type'] = CSRAttributeType('extension_request')
    extension_cri_attr['values'] = extensions_set
    cri_attributes.append(extension_cri_attr)

    cri['attributes'] = cri_attributes

    # Create CSR
    pkcs10 = CertificationRequestNullSigned()
    pkcs10['certification_request_info'] = cri

    signature_algorithm = DigestAlgorithm()
    signature_algorithm['algorithm'] = DigestAlgorithmId('sha256')
    pkcs10['signature_algorithm'] = signature_algorithm

    pkcs10['signature'] = OctetBitString(sha256(cri.dump()).digest())

    return pkcs10


def create_pki_data(pkcs10):
    pki_data = PKIData()

    tagged_csr = TaggedCertificationRequest()
    tagged_csr['bodyPartID'] = 0
    tagged_csr['certificationRequest'] = pkcs10
    tagged_request = TaggedRequest({'tcr': tagged_csr})
    tagged_requests = TaggedRequests()
    tagged_requests.append(tagged_request)

    tagged_attributes = TaggedAttributes(SequenceOf())
    tagged_content_infos = TaggedContentInfos(SequenceOf())
    other_msgs = OtherMsgs(SequenceOf())

    pki_data['controlSequence'] = tagged_attributes
    pki_data['reqSequence'] = tagged_requests
    pki_data['cmsSequence'] = tagged_content_infos
    pki_data['otherMsgSequence'] = other_msgs

    return pki_data


def create_encap_content_info(pki_data):
    encap_content_info = EncapsulatedContentInfo()
    encap_content_info['content_type'] = ContentType.map('1.3.6.1.5.5.7.12.2')
    encap_content_info['content'] = ParsableOctetString(pki_data.dump())
    return encap_content_info


def create_signed_attributes(eci_content):
    signed_attributes = CMSAttributes()
    attribute_content_type = CMSAttribute()
    attribute_content_type['type'] = '1.2.840.113549.1.9.3'  # PKCS#9 content type
    attribute_content_type['values'] = ['1.3.6.1.5.5.7.12.2']

    attribute_message_digest = CMSAttribute()
    attribute_message_digest['type'] = '1.2.840.113549.1.9.4'  # message digest
    attribute_message_digest['values'] = [OctetString(sha256(eci_content.native).digest())]

    signed_attributes.append(attribute_content_type)
    signed_attributes.append(attribute_message_digest)

    return signed_attributes


def create_signer_infos(ca_name, eci_content):
    signer_info = SignerInfo()
    signer_info['version'] = CMSVersion(1)  # because the sid is issuer_and_serial_number

    # Issuer is the name of certification authority, serial number is a random number,
    # since the signer certificate is not present
    issuer_and_serial_number = IssuerAndSerialNumber()
    issuer_and_serial_number['issuer'] = Name.build({'common_name': ca_name})
    issuer_and_serial_number['serial_number'] = 123456789
    signer_info['sid'] = issuer_and_serial_number

    digest_algorithm = DigestAlgorithm()
    digest_algorithm['algorithm'] = DigestAlgorithmId('sha256')
    digest_algorithm['parameters'] = None
    signer_info['digest_algorithm'] = digest_algorithm

    signed_attributes = create_signed_attributes(eci_content)
    signer_info['signed_attrs'] = signed_attributes

    signature_algorithm = SignedDigestAlgorithm()
    signature_algorithm['algorithm'] = '1.3.6.1.5.5.7.6.2'
    signature_algorithm['parameters'] = Null()
    signer_info['signature_algorithm'] = signature_algorithm

    signer_info['signature'] = OctetString(sha256(signed_attributes.dump()).digest())

    signer_infos = SignerInfos()
    signer_infos.append(signer_info)

    return signer_infos


def create_signed_data(pki_data, ca_name):
    signed_data = SignedData()
    signed_data['version'] = CMSVersion(3)

    digest_algorithms = DigestAlgorithms()
    digest_algorithm = DigestAlgorithm()
    digest_algorithm['algorithm'] = DigestAlgorithmId('sha256')
    digest_algorithm['parameters'] = None
    digest_algorithms.append(digest_algorithm)

    signed_data['digest_algorithms'] = digest_algorithms
    signed_data['encap_content_info'] = create_encap_content_info(pki_data)
    signed_data['signer_infos'] = create_signer_infos(ca_name, signed_data['encap_content_info']['content'])

    return signed_data
