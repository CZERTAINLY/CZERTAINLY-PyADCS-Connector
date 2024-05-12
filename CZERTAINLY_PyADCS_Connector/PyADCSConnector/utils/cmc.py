from asn1crypto import csr
from asn1crypto._errors import unwrap
from asn1crypto._types import int_types, type_name
from asn1crypto.algos import DigestAlgorithm
from asn1crypto.cms import ContentInfo
from asn1crypto.core import Sequence, SequenceOf, ObjectIdentifier, Choice, SetOf, OctetString, Any, OctetBitString, \
    Integer
from asn1crypto.csr import CertificationRequest

from PyADCSConnector.utils.crmf import CertReqMsg, CertificationRequestNullSigned


class AttributeValueOid(ObjectIdentifier):
    _map = [
        {'id-cmc 18', 'regInfo'}
    ]


class AttributeValue(Any):
    pass


class AttributeValueSet(SetOf):
    _child_spec = AttributeValue


class TaggedAttribute(Sequence):
    _fields = [
        ('bodyPartID', Integer),
        ('attrType', AttributeValueOid),
        ('attrValues', AttributeValueSet)
    ]


class TaggedAttributes(SequenceOf):
    _child_spec = TaggedAttribute


class TaggedCertificationRequest(Sequence):
    _fields = [
        ('bodyPartID', Integer),
        ('certificationRequest', CertificationRequestNullSigned)
    ]


class TaggedRequest(Choice):
    _alternatives = [('tcr', TaggedCertificationRequest, {'implicit': 0}),
                     ('crm', CertReqMsg, {'implicit': 1})
                     ]


class TaggedRequests(SequenceOf):
    _child_spec = TaggedRequest


class TaggedContentInfo:
    _fields = [('bodyPartID', 0),
               ('contentInfo', ContentInfo)
               ]


class TaggedContentInfos(SequenceOf):
    _child_spec = TaggedContentInfo


class OtherMsg(Sequence):
    _fields = [('bodyPartID', 0),
               ('otherMsgType', ObjectIdentifier),
               ('otherMsgValue', Any)]


class OtherMsgs(SequenceOf):
    _child_spec = OtherMsg


class PKIData(Sequence):
    _fields = [
        ('controlSequence', TaggedAttributes,  {'optional': True}),
        ('reqSequence', TaggedRequests),
        ('cmsSequence', TaggedContentInfos, {'optional': True}),
        ('otherMsgSequence', OtherMsgs, {'optional': True})
    ]
