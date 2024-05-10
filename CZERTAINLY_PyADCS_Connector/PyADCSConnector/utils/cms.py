from asn1crypto.algos import DigestAlgorithm, SignedDigestAlgorithm, AlgorithmIdentifier
from asn1crypto.cms import EncapsulatedContentInfo, RevocationInfoChoices, CertificateSet, \
    DigestAlgorithms, CMSVersion, CMSAttributes, IssuerAndSerialNumber, ContentType
from asn1crypto.core import Sequence, SequenceOf, OctetString, Choice, SetOf


class SignerIdentifier(Choice):
    _alternatives = [
        ('issuer_and_serial_number', IssuerAndSerialNumber),
        ('subject_key_identifier', AlgorithmIdentifier, {'implicit': 0}),
    ]


class SignerInfo(Sequence):
    _fields = [
        ('version', CMSVersion),
        ('sid', SignerIdentifier),
        ('digest_algorithm', DigestAlgorithm),
        ('signed_attrs', CMSAttributes, {'implicit': 0, 'optional': True}),
        ('signature_algorithm', SignedDigestAlgorithm),
        ('signature', OctetString),
        ('unsigned_attrs', CMSAttributes, {'implicit': 1, 'optional': True}),
    ]


class SignerInfos(SetOf):
    _child_spec = SignerInfo


class SignedData(Sequence):
    _fields = [
        ('version', CMSVersion),
        ('digest_algorithms', DigestAlgorithms),
        ('encap_content_info', EncapsulatedContentInfo),
        ('certificates', CertificateSet, {'implicit': 0, 'optional': True}),
        ('crls', RevocationInfoChoices, {'implicit': 1, 'optional': True}),
        ('signer_infos', SignerInfos),
    ]


class ContentInfo(Sequence):
    _fields = [
        ('content_type', ContentType),
        ('content', SignedData, {'explicit': 0, 'optional': True}),
    ]

    _oid_pair = ('content_type', 'content')
    _oid_specs = {}