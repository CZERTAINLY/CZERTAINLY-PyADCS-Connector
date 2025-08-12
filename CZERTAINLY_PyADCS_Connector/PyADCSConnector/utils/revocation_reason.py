from enum import Enum


class CertificateRevocationReason(Enum):
    UNSPECIFIED = "unspecified"
    KEY_COMPROMISE = "keyCompromise"
    CA_COMPROMISE = "cACompromise"
    AFFILIATION_CHANGED = "affiliationChanged"
    SUPERSEDED = "superseded"
    CESSATION_OF_OPERATION = "cessationOfOperation"
    CERTIFICATE_HOLD = "certificateHold"
    REMOVE_FROM_CRL = "removeFromCRL"
    PRIVILEGES_WITHDRAWN = "privilegeWithdrawn"
    AA_COMPROMISE = "aACompromise"

    @staticmethod
    def from_string(reason: str) -> 'CertificateRevocationReason':
        return {
            "unspecified": CertificateRevocationReason.UNSPECIFIED,
            "keyCompromise": CertificateRevocationReason.KEY_COMPROMISE,
            "cACompromise": CertificateRevocationReason.CA_COMPROMISE,
            "affiliationChanged": CertificateRevocationReason.AFFILIATION_CHANGED,
            "superseded": CertificateRevocationReason.SUPERSEDED,
            "cessationOfOperation": CertificateRevocationReason.CESSATION_OF_OPERATION,
            "certificateHold": CertificateRevocationReason.CERTIFICATE_HOLD,
            "removeFromCRL": CertificateRevocationReason.REMOVE_FROM_CRL,
            "privilegeWithdrawn": CertificateRevocationReason.PRIVILEGES_WITHDRAWN,
            "aACompromise": CertificateRevocationReason.AA_COMPROMISE
        }.get(reason, CertificateRevocationReason.UNSPECIFIED)

    def to_string_ps_value(self) -> str:
        return {
            CertificateRevocationReason.UNSPECIFIED: "Unspecified",
            CertificateRevocationReason.KEY_COMPROMISE: "KeyCompromise",
            CertificateRevocationReason.CA_COMPROMISE: "CACompromise",
            CertificateRevocationReason.AFFILIATION_CHANGED: "AffiliationChanged",
            CertificateRevocationReason.SUPERSEDED: "Superseded",
            CertificateRevocationReason.CESSATION_OF_OPERATION: "CeaseOfOperation",
            CertificateRevocationReason.CERTIFICATE_HOLD: "Hold",
            CertificateRevocationReason.REMOVE_FROM_CRL: "RemoveFromCRL",
            CertificateRevocationReason.PRIVILEGES_WITHDRAWN: "Unspecified",
            CertificateRevocationReason.AA_COMPROMISE: "Unspecified"
        }.get(self, "Unspecified")

    def to_code(self) -> int:
        return {
            CertificateRevocationReason.UNSPECIFIED: 0,
            CertificateRevocationReason.KEY_COMPROMISE: 1,
            CertificateRevocationReason.CA_COMPROMISE: 2,
            CertificateRevocationReason.AFFILIATION_CHANGED: 3,
            CertificateRevocationReason.SUPERSEDED: 4,
            CertificateRevocationReason.CESSATION_OF_OPERATION: 5,
            CertificateRevocationReason.CERTIFICATE_HOLD: 6,
            CertificateRevocationReason.REMOVE_FROM_CRL: 8,
            CertificateRevocationReason.PRIVILEGES_WITHDRAWN: 9,
            CertificateRevocationReason.AA_COMPROMISE: 10
        }.get(self, 0)
