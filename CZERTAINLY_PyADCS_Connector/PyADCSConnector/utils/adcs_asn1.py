from asn1crypto.cms import ContentInfo
from asn1crypto.cms import ContentInfo
from asn1crypto.core import Sequence, SequenceOf, ObjectIdentifier, Choice, SetOf, Any, Integer

from PyADCSConnector.utils.crmf import CertReqMsg, CertificationRequestNullSigned


class CertificateTemplateOid(Sequence):
    _fields = [
        ('templateID', ObjectIdentifier),
        ('templateMajorVersion', Integer, {'optional': True}),
        ('templateMinorVersion', Integer, {'optional': True})
    ]
