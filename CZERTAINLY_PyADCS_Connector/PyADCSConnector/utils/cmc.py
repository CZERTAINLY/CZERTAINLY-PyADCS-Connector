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
    _alternatives = [('tcr', TaggedCertificationRequest),
                     ('crm', CertReqMsg)
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


class SequenceCustom(Sequence):
    def __setitem__(self, key, value):
        """
        Allows settings fields by name or index

        :param key:
            A unicode string of the field name, or an integer of the field index

        :param value:
            A native Python datatype to set the field value to. This method will
            construct the appropriate Asn1Value object from _fields.

        :raises:
            ValueError - when a field name or index is invalid
        """

        # We inline this check to prevent method invocation each time
        if self.children is None:
            self._parse_children()

        if not isinstance(key, int_types):
            if key not in self._field_map:
                raise KeyError(unwrap(
                    '''
                    No field named "%s" defined for %s
                    ''',
                    key,
                    type_name(self)
                ))
            key = self._field_map[key]

        field_name, field_spec, value_spec, field_params, _ = self._determine_spec(key)

        new_value = self._make_value(field_name, field_spec, value_spec, field_params, value)

        invalid_value = False
        if isinstance(new_value, Any):
            invalid_value = new_value.parsed is None

        if invalid_value:
            raise ValueError(unwrap(
                '''
                Value for field "%s" of %s is not set
                ''',
                field_name,
                type_name(self)
            ))

        self.children[key] = new_value

        if self._native is not None:
            self._native[self._fields[key][0]] = self.children[key].native
        self._mutated = True


class PKIData(SequenceCustom):
    _fields = [
        ('controlSequence', TaggedAttributes,  {'optional': True}),
        ('reqSequence', TaggedRequests),
        ('cmsSequence', TaggedContentInfos, {'optional': True}),
        ('otherMsgSequence', OtherMsgs, {'optional': True})
    ]
