import winrm
from django.test import TestCase

from PyADCSConnector.remoting.winrm.scripts import IMPORT_FUNCTION_CONVERT_RAWCERTTOBYTES, IMPORT_FUNCTION_APPLY_FILTERS
from PyADCSConnector.remoting.winrm_remoting import minify_ps
from PyADCSConnector.utils.dump_parser import DumpParser


class DumpParserTest(TestCase):
    def test_parse_certificates(self):
        data = """

RequestID                  : 710
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 7/7/2023 9:35:52 AM
Request.CommonName         :
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.2517003.8444064
RawCertificate             : MIIG0DCCBLigAwIBAgITGAAAAsaadzCSgw33agAAAAACxjANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzA3MDcwOTI1NTJaFw0yNDA3MDYwOTI1NTJaMIGEMRUw
                             EwYKCZImiZPyLGQBGRYFbG9jYWwxFDASBgoJkiaJk/IsZAEZFgQza2V5MQ4wDAYD
                             VQQDEwVVc2VyczEbMBkGA1UEAwwSTsSbamFrw70gVcW+aXZhdGVsMSgwJgYJKoZI
                             hvcNAQkBFhltaWNoYWwudHV0a29AM2tleS5jb21wYW55MIIBIjANBgkqhkiG9w0B
                             AQEFAAOCAQ8AMIIBCgKCAQEAlCT+JtEnPTmsjvBwecsaNmwEiJxmC6QzCrlcppuE
                             buGlGBopaSI0JaAutLpNd8rfzlaPX20x0AvHCiFEHHopISsx/brxkgEax3wpfdDO
                             jmtHGOwklPW1W76ooY8qI6fRfn0gUVi338nxI+KWwxIZCItu23ZPEfoCwPNfUtLc
                             rHc32ZiA7IZqv88vgH12LAScjB0E/Fd/Udt2tOaSNt4u/eUMBcYvybRWEaPhsU4x
                             lBhVvO1V57LGMhe5L4p9AhCxaY+cF1zeRhznm5RMTSm1dNS2gyZrioZa7i2SUJl9
                             zXY3mGFl7fpVQFk48Bu8rnJ7yWacvSE5ZlgFsO/dvA5wEQIDAQABo4IChTCCAoEw
                             PQYJKwYBBAGCNxUHBDAwLgYmKwYBBAGCNxUIh+WDYaiHcIKJgTyEk8IBhYi5aoFM
                             gZnQC4SDsSACAWQCAQMwKQYDVR0lBCIwIAYIKwYBBQUHAwIGCCsGAQUFBwMEBgor
                             BgEEAYI3CgMEMA4GA1UdDwEB/wQEAwIFoDA1BgkrBgEEAYI3FQoEKDAmMAoGCCsG
                             AQUFBwMCMAoGCCsGAQUFBwMEMAwGCisGAQQBgjcKAwQwRAYJKoZIhvcNAQkPBDcw
                             NTAOBggqhkiG9w0DAgICAIAwDgYIKoZIhvcNAwQCAgCAMAcGBSsOAwIHMAoGCCqG
                             SIb3DQMHMB0GA1UdDgQWBBSeqeR6QySEWQ1Qc4pXyG73AvaxaDAfBgNVHSMEGDAW
                             gBSSwrzfVcXBk4VJB/esyR0LaAEHUTBNBgNVHR8ERjBEMEKgQKA+hjxodHRwOi8v
                             bGFiMDIuM2tleS5jb21wYW55L2NybHMvZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBD
                             QS5jcmwwVwYIKwYBBQUHAQEESzBJMEcGCCsGAQUFBzABhjtodHRwOi8vbGFiMDIu
                             M2tleS5jb21wYW55L2Nhcy9kZW1vL0RlbW8lMjBNUyUyMFN1YiUyMENBLmNydDBQ
                             BgNVHREESTBHoCoGCisGAQQBgjcUAgOgHAwabmVqYWt5LnV6aXZhdGVsQDNrZXku
                             bG9jYWyBGW1pY2hhbC50dXRrb0Aza2V5LmNvbXBhbnkwTgYJKwYBBAGCNxkCBEEw
                             P6A9BgorBgEEAYI3GQIBoC8ELVMtMS01LTIxLTM4MjAwMjQ4NTctMjY5NTcxMTA5
                             OS00NTA5NTgwMzgtMTYxODANBgkqhkiG9w0BAQ0FAAOCAgEAUrWqJxH0CT2ydNjx
                             f2UWwYJdy+JNKK/nWG9WOphqd/18Dnr5Ed4zehvEXoXOdme2uypc0h6xffNSZMUy
                             D8hd0hjF5qS4jxSX6pqhhoiUHedESaJj47yvkWV3TLUh+YUb1cgwOP3F2g+zSQzV
                             GqhaXJjiL8zV49PmGoEVwsuAMGIsC5BIsv+G3EXMc0la3L5AgI2c1c50fbgrmOhM
                             1Cy5K7BpgdMKnUrzTv1ayMhKy+0wdCj77QzihEXJGSRVqqeS+NiloKwHBRq2GWn6
                             ABzAy+x7tqj3qGPnCyl3W9TD8DBv+ljIYgOuCxHMdZPruPvu1I+luUy9a6WD2B/F
                             ImI4gvK3RkqDbnUUOITy1j5cCvg3z9HWil8p5420VJ1LLSpHg5Tee5+ZiTf2tQnk
                             jypHbt7hTfDwJKmdh1wB+H8dhmFGLDYDB3cS2/QQuauWzUFjKQVtSoOe2LhWfO36
                             Huz2Lkmq6Ic0ALsyc/As33K8ot59PDQLwDVZuSIrY03VrSLMmqvc6+ryy0lmxI/K
                             K8WEa5tN6DCKE0F8EdZ4W/gZC2633uxgxklXZ8bP7eVZo8eC08/0+lJd0lxVrCWp
                             rbK5G6raNl0gxum4cdly1xFB1zyT1cge3Hnka9S3hocnyYPBpa/oDlUh8vjq2gK9
                             XcG0+T+/UgTeq7Sg6nNfZDZdkIk=

CertificateTemplateOid     : Certificate authentication external client
                             (1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.2517003.8444064)
RowId                      : 710
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 710], [Request.StatusCode, 0], [Request.DispositionMessage, Issued],
                             [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}

RequestID                  : 716
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 8/18/2023 9:56:15 AM
Request.CommonName         : Michal Zitko
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.2517003.8444064
RawCertificate             : MIIG0DCCBLigAwIBAgITGAAAAsw25Qj4eR6dMQAAAAACzDANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzA4MTgwOTQ2MTVaFw0yNDA4MTcwOTQ2MTVaMIGEMRUw
                             EwYKCZImiZPyLGQBGRYFbG9jYWwxFDASBgoJkiaJk/IsZAEZFgQza2V5MQ4wDAYD
                             VQQDEwVVc2VyczEbMBkGA1UEAwwSTsSbamFrw70gVcW+aXZhdGVsMSgwJgYJKoZI
                             hvcNAQkBFhltaWNoYWwudHV0a29AM2tleS5jb21wYW55MIIBIjANBgkqhkiG9w0B
                             AQEFAAOCAQ8AMIIBCgKCAQEAyql/vxeDtOrNXCjhBvJhr/v5MAS5zLZeLG8Znepa
                             DO/3LDQU344rZbqN/LJw1i0Z4KpPaasQVMV9QS3WimsFcTS7xmCnFKf2zlzCnTis
                             wkiv1MxktbTN1f+a3sdMxxKbx+7ILoVvPNSUSz70PJIAeJOLbB4aSogx8NY3KMg4
                             yRJtzv0KpzNgs4P3bEB/wZdMhzCSxzA6zqHVdllBGUIL6KN/Afe84BAx75FRmfrM
                             vQUrX70eQgFU+6faeNI19H6tg8qT1uirrSg/CO2rtyECzGELbrxE1Dnm4JdZ5237
                             9pA9n5atg3o7Qh8AChZzwQYf3YmzA3UfqA0xSV0tPfYtEQIDAQABo4IChTCCAoEw
                             HQYDVR0OBBYEFBJBHJrSR1Tindvn0QRUE8zuMtjgMB8GA1UdIwQYMBaAFJLCvN9V
                             xcGThUkH96zJHQtoAQdRME0GA1UdHwRGMEQwQqBAoD6GPGh0dHA6Ly9sYWIwMi4z
                             a2V5LmNvbXBhbnkvY3Jscy9kZW1vL0RlbW8lMjBNUyUyMFN1YiUyMENBLmNybDBX
                             BggrBgEFBQcBAQRLMEkwRwYIKwYBBQUHMAGGO2h0dHA6Ly9sYWIwMi4za2V5LmNv
                             bXBhbnkvY2FzL2RlbW8vRGVtbyUyME1TJTIwU3ViJTIwQ0EuY3J0MA4GA1UdDwEB
                             /wQEAwIFoDA9BgkrBgEEAYI3FQcEMDAuBiYrBgEEAYI3FQiH5YNhqIdwgomBPIST
                             wgGFiLlqgUyBmdALhIOxIAIBZAIBBDApBgNVHSUEIjAgBggrBgEFBQcDAgYIKwYB
                             BQUHAwQGCisGAQQBgjcKAwQwNQYJKwYBBAGCNxUKBCgwJjAKBggrBgEFBQcDAjAK
                             BggrBgEFBQcDBDAMBgorBgEEAYI3CgMEMFAGA1UdEQRJMEegKgYKKwYBBAGCNxQC
                             A6AcDBpuZWpha3kudXppdmF0ZWxAM2tleS5sb2NhbIEZbWljaGFsLnR1dGtvQDNr
                             ZXkuY29tcGFueTBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQtUy0x
                             LTUtMjEtMzgyMDAyNDg1Ny0yNjk1NzExMDk5LTQ1MDk1ODAzOC0xNjE4MEQGCSqG
                             SIb3DQEJDwQ3MDUwDgYIKoZIhvcNAwICAgCAMA4GCCqGSIb3DQMEAgIAgDAHBgUr
                             DgMCBzAKBggqhkiG9w0DBzANBgkqhkiG9w0BAQ0FAAOCAgEABKsm0OiHTXht+nr6
                             6/ayMgERYWQ3QOw68FGlJSL9GqhMTYu9/cFJVm4yoIIm35w+7YWCqzpxHU35V3Ky
                             xxKZ4EFiBorligIvmeEec+YIrw6yKnbQpxHi9qAgOk1zUJWWKU65L/ifH7o9BZHT
                             KzFf8563QZVXQY/SOiLEqKtSgtDd+o70xywHmOz7egzuX7lfI5uERf5iiIqqQZCJ
                             UMy7y7eP88/Nqt/ZhQvDXMdCO+DuQ+VqbBcDMFwD9NAsGKqHkXVkumPEynINZh3f
                             otcGlQQhJDfiSsGJC46ToStX/f1Zn7sgRDgv+zQlQi2GlAOVQrJd/2x1qESKXc+9
                             IWRlGtd1vqrHH2r9n4mkgp39kz9f+LPErFo1tDXVfMfHNfT9dVWcrXiXL79pNfRJ
                             2ZjtccPcJPsjSFJn9jmVZgVDgi4JFsDkxiDKfhh23PrQ1fkwAuCd9BtnAi4bqH9W
                             9m0SrEY34W4dEplldOplPYiGLSTnJeSXwP3Ip0Qz2ZyEATPc0NZHN82S0RMbB4TJ
                             N9uqAjv9aubVMlKUcdZ6ZRmYWLi0PEfFuB3cI5qVqqP2S8+QpeaHg3XncUfXSvnL
                             cZIPDedc8EP2gUmZY8cpXaHOLlu3624VBSD92AsXnvUFCiawETWeUdcrv40R0XfO
                             CnvWrdJxVXh1pfmRF9Rcu76M9KU=

CertificateTemplateOid     : Certificate authentication external client
                             (1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.2517003.8444064)
RowId                      : 716
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 716], [Request.StatusCode, 0], [Request.DispositionMessage, Issued],
                             [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}

RequestID                  : 787
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\VMI307469$
Request.SubmittedWhen      : 12/28/2023 12:26:31 PM
Request.CommonName         : lab02.3key.company
CertificateTemplate        : WebServer
RawCertificate             : MIIFNjCCAx6gAwIBAgITGAAAAxP9YXII0BMNqQAAAAADEzANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzEyMjgxMjE2MzFaFw0yNTEyMjcxMjE2MzFaMB0xGzAZ
                             BgNVBAMTEmxhYjAyLjNrZXkuY29tcGFueTCCASIwDQYJKoZIhvcNAQEBBQADggEP
                             ADCCAQoCggEBAK5b2H5I8iJOYNxWSRah3rDUz9BPjADu2OjvlNhqJqJ3vFNyPlms
                             GHmtWb1SvQAjZGRdIF+hC1YSchs/u4mq5XxBMCjI6b9Ne2o8slkDobDaHhwAJCRt
                             9RuVr+goVIM+WovNEexlgK/7fScV9Nej0+pzu0tT1vIwiZU81O12ebg3Lg7LaLsM
                             91Vefhs8Tc+tF8hfnvZ2ywWCEvx0kQD8OP6bjhoVOe/hgx9bhksI0aJg7db1dbLC
                             sbr/z6vOEj3E7jH1zxNQ6iPQ3sPvaf/+kCHOSoJjpImkQiq0evYCdeSR/NNTc+Hq
                             b3tcYVIBhQI2dgbj1c9xe4omyp7F3XJZdj0CAwEAAaOCAVMwggFPMCEGCSsGAQQB
                             gjcUAgQUHhIAVwBlAGIAUwBlAHIAdgBlAHIwEwYDVR0lBAwwCgYIKwYBBQUHAwEw
                             DgYDVR0PAQH/BAQDAgWgMB0GA1UdDgQWBBTcDLXCwo8HCKLOPY2JKoDIzgjZ7zAd
                             BgNVHREEFjAUghJsYWIwMi4za2V5LmNvbXBhbnkwHwYDVR0jBBgwFoAUksK831XF
                             wZOFSQf3rMkdC2gBB1EwTQYDVR0fBEYwRDBCoECgPoY8aHR0cDovL2xhYjAyLjNr
                             ZXkuY29tcGFueS9jcmxzL2RlbW8vRGVtbyUyME1TJTIwU3ViJTIwQ0EuY3JsMFcG
                             CCsGAQUFBwEBBEswSTBHBggrBgEFBQcwAYY7aHR0cDovL2xhYjAyLjNrZXkuY29t
                             cGFueS9jYXMvZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBDQS5jcnQwDQYJKoZIhvcN
                             AQENBQADggIBALAVZ8r9Z6lDmiui3FhD3RdfghLENLUB+SBbDtDNg/+udKFLdU7l
                             eaew2pPi/SoPFZOMKAW5lC5Iq0MXCeppTe/gvE6Q8+doJ6RqEQwtpSYkG3zZjnEX
                             qYoeWBu0QFIYueuYlvPret3t8whTZt32wCDPyOp6ks1jDa2WMRKge+1xs4bBUFBn
                             wMqlifBUf9ulNlaVTW0Y32zluqlGiKnbrHSveJ3TBUbG7sbqhQ6XB1AfZIwCK5JQ
                             yLI3WAnNr1ziFlvERZzYrYDHviBYtdOZgp+ttmeT3XddrMXliklRGQ5Rl9O8EL5T
                             Dg9ViXM3PH04g6Ce84oJXevy7Ohxdok7JvdKA74fsfbRYM6ZP5AftXt3apmF0GoO
                             gbU7Y9z9q+7w++BX0e61cNdmHGOpxZa7OKLGhNel86lVgPeggY+PdYyfp+18v3je
                             /0z5vHR3pmcBqbrYP0JZj/XHVYNyXTf6ba2I/xiABTux/ntQIVbKHZTT/oVwuYa6
                             ISCJ9GKFKoB1u3MmDx2zAHESaTJmrAQZc259cCnUuboR37L83v00Px6MfAmo8yfX
                             n65WTcqigQBOfWCOlJsRKS+q56+zRTotSxTaBQbnsloCS8Xw9x9pHfWRk5x6A5ew
                             k+c+s1LmTHr6WQF7NlwiG1rQ859i2hw7Fnlxd/2ro25EfD79Q55ZOU6H
                             
CertificateTemplateOid     : WebServer
RowId                      : 787
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 787], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], 
                             [Request.RequesterName, 3KEY\\VMI307469$]...}
RequestID                  : 788
Request.StatusCode         : 0
Request.DispositionMessage : Revoked by 3KEY\\nejaky.uzivatel
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 12/30/2023 2:17:34 PM
Request.CommonName         : signserver-ra-01
CertificateTemplate        : WebServer
RawCertificate             : MIIFFTCCAv2gAwIBAgITGAAAAxSPMU0RrjbifAAAAAADFDANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzEyMzAxNDA3MzRaFw0yNTEyMjkxNDA3MzRaMBsxGTAX
                             BgNVBAMTEHNpZ25zZXJ2ZXItcmEtMDEwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
                             ggEKAoIBAQCgyWCtOYPVN45+tIyWg1bkTtVHew5dtAV6cJkHnfTYFo0MFMIs0US1
                             DnSZmMZUaUL73Ic6M9YDmsSdjEh4BiwJIBmKSy6lkg0lxOEzqYmu0K0YEBm3JjMY
                             l/fkPl+bre28xY5a9U5f1l3BVufxdR1+h7dlnSyaDMp2b8CqD3icr+4LO2HzOpwS
                             FlrMPuPf+uM58G2GeQsnePjxyDaRfIO58v064AcqB8OPLBq34J4D15RsGz5HtS9Y
                             RWSrzy0HFt3ipHzcaUucLnVTBeYpZKBl64+k4LAYINNq8hsb9TbVdvu8f3d1fXdB
                             32DJduOfnUBPB/Hz3sktPd/77i67FUoPAgMBAAGjggE0MIIBMDAdBgNVHQ4EFgQU
                             +/jrrO9jvD3ecJdurHKYa83v/MYwHwYDVR0jBBgwFoAUksK831XFwZOFSQf3rMkd
                             C2gBB1EwTQYDVR0fBEYwRDBCoECgPoY8aHR0cDovL2xhYjAyLjNrZXkuY29tcGFu
                             eS9jcmxzL2RlbW8vRGVtbyUyME1TJTIwU3ViJTIwQ0EuY3JsMFcGCCsGAQUFBwEB
                             BEswSTBHBggrBgEFBQcwAYY7aHR0cDovL2xhYjAyLjNrZXkuY29tcGFueS9jYXMv
                             ZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBDQS5jcnQwIQYJKwYBBAGCNxQCBBQeEgBX
                             AGUAYgBTAGUAcgB2AGUAcjAOBgNVHQ8BAf8EBAMCBaAwEwYDVR0lBAwwCgYIKwYB
                             BQUHAwEwDQYJKoZIhvcNAQENBQADggIBAMS6CoozrYDB0EBstl7lJiCK4ki6Ixpl
                             HCJZCQRatyMvUu48/cTDwPz+nNsDFuO691+6R3f0RJ5gsvtLyP0l+/h0IuK7DMOa
                             Tx8/k8xaHh5LXGcmkr5JREXgCqq35kImWfprsNEZ7HBDT24WmTedhy3L61igwlOY
                             82f1IA3ZAZ/jyoOnRV0mo1xmzyvUQ0WWlprGFeeE5YymaZeCWpLDdhrwOPP9iFcf
                             pNXc+mlPdG4NXUA+BKzZ0pM0J7VnSr9Vbnk6iSzAQFCEQFDee7v7gJr6tzpmoSWR
                             QUghA0cVlKg9ETx0jor+Uv6nJqPW/nusfn7Nx0sX/Ieh+At6OXa5wXJ09Y6GAz64
                             qudqBskp5mMtxFocmG6nHseo9wA3W8bQaoJYW+yyOqQhRGd1BuCsLYLR/M1n76of
                             ANSC3ZRkWdImsGZbqrCB5CcjOG9VTbVkO+O1kCp9uu0AALp+87firfOG7ggVWWkx
                             sCL0PuR/QuWlXsXSh2qFx/2MF/834tCRozbAOlBhY3WAzesvsBpZtEI/nkZSWe7a
                             kDY6gmYk71kjmKqxrw8CIzDVa+pWe6/TuMuwnVUttLOLsu7rSY26pBte8sMtf+Gn
                             yXmIwqYWDUtjhA7tjE1gtVK19z3MKUQg0zPTcphikOcxps+nVrUNvzCS6/Mnu88l
                             yR3kZc7dtNpz
                             
CertificateTemplateOid     : WebServer
RowId                      : 788
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 788], [Request.StatusCode, 0], [Request.DispositionMessage, Revoked by 
                             3KEY\\nejaky.uzivatel], [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}
RequestID                  : 789
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 12/31/2023 9:33:55 AM
Request.CommonName         : testpy
CertificateTemplate        : WebServer
RawCertificate             : MIIEhzCCAm+gAwIBAgITGAAAAxVSi91EVbaymgAAAAADFTANBgkqhkiG9w0BAQ0F
                             ADA3MRcwFQYDVQQDDA5EZW1vIE1TIFN1YiBDQTEcMBoGA1UECgwTM0tleSBDb21w
                             YW55IHMuci5vLjAeFw0yMzEyMzEwOTIzNTVaFw0yNTEyMzAwOTIzNTVaMBExDzAN
                             BgNVBAMTBnRlc3RweTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAtKU1kDjC
                             x9U8bN+YY6CKI9mkxd1K7Z7K6gbcyIJ1pC+M53ONRe59p2JD9zfgJRbkQTilzffO
                             hfmFebEMq0Lt0OJdP1TOD9BtlA3Sc0QVKya46JfpEY8oYHq05JDV/kMQWaJPiDhk
                             6/m6hzQx8egKcv/8G4dvHBcDOfuY28cldAECAwEAAaOCATQwggEwMB0GA1UdDgQW
                             BBQKmJn706mQCPOnGyC6I/oHUMBf5jAfBgNVHSMEGDAWgBSSwrzfVcXBk4VJB/es
                             yR0LaAEHUTBNBgNVHR8ERjBEMEKgQKA+hjxodHRwOi8vbGFiMDIuM2tleS5jb21w
                             YW55L2NybHMvZGVtby9EZW1vJTIwTVMlMjBTdWIlMjBDQS5jcmwwVwYIKwYBBQUH
                             AQEESzBJMEcGCCsGAQUFBzABhjtodHRwOi8vbGFiMDIuM2tleS5jb21wYW55L2Nh
                             cy9kZW1vL0RlbW8lMjBNUyUyMFN1YiUyMENBLmNydDAhBgkrBgEEAYI3FAIEFB4S
                             AFcAZQBiAFMAZQByAHYAZQByMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggr
                             BgEFBQcDATANBgkqhkiG9w0BAQ0FAAOCAgEAmXVJl3otyFcoUrr/UhjBJXmpg+iv
                             tRLhDKPoVSKbMCSY2tBSGeQ9V3kE5+KQI+om1plTXKQBgHaFOGamq3K1DytjEJuK
                             TkwmWU4QVmkCYwv1qYEMQ5gqGWU1BDhuS43Q5oTR7Hv2G/dGxGaZDNycXE5aT/7T
                             X7KJlIL5bC63i0ng2NVjhgqmHLRP48K0T8e3sX0jRRDKbpAVY04VBOv4WSr6M7sn
                             Ib626eXEs96JgKnRp6wIJRwvbaBJdfJZpFBmBwTBzPjmNt+29+IDYHt3rQOA46Dg
                             SEKTOwptKgZzXHig1kVtM/8eebyIV8wls5HwOfQ2VTc/uPjrouD9SAW76wQLjvZd
                             14py+SafebFvEch//4QJhrPqYV5i7X3naFEIbtosDCvocT3eqq2FgWQAKzg84UJR
                             3bo6n5mWXIDoWwxdTdrbzxmYkPbIZpiGJhtHIbYJpxZHrbH7pma43Rtoo2PPXnl6
                             ORaTIFdYcOmff11foa/8QbyzgNSzDlxeUcbKaS/vjiPgY+/QPsc7KUVTVbrd3jIB
                             sc8BgWEMXzIEqBGZixNnJrpavZW9u9E2AhhztUjGd84Ok77bUeCgE620NyKrIZOx
                             F4D6SjYGvPiXdWEkVWKVYO6ego/GSYEzzFqwKWnp+EDnaj+8Vjc3LYD01WtPucDz
                             BkciW85+HYbHuwE=
                             
CertificateTemplateOid     : WebServer
RowId                      : 789
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 789], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], 
                             [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_certificates(result)
        self.assertEqual(len(templates), 5)
        self.assertEqual(templates[2].template, "WebServer")

    def test_parse_template(self):
        data = """
        
Name          : TestofEnrollmentAgent
DisplayName   : Test of Enrollment Agent
SchemaVersion : 4
Version       : 100.3
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.8007785.10868302

Name          : User
DisplayName   : User
SchemaVersion : 1
Version       : 3.1
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.1

Name          : UserSignature
DisplayName   : User Signature Only
SchemaVersion : 1
Version       : 4.1
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.2

Name          : WebServer
DisplayName   : Web Server
SchemaVersion : 1
Version       : 4.1
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.16

Name          : Workstation
DisplayName   : Workstation Authentication
SchemaVersion : 2
Version       : 101.0
OID           : 1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.30

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_template_data(result)
        self.assertEqual(len(templates), 5)
        self.assertEqual(templates[0].name, "TestofEnrollmentAgent")
        self.assertEqual(templates[1].display_name, "User")
        self.assertEqual(templates[2].schema_version, "1")
        self.assertEqual(templates[3].version, "4.1")
        self.assertEqual(templates[4].oid, "1.3.6.1.4.1.311.21.8.16335329.656368.4341948.8708353.10624234.204.1.30")

    def test_parse_identified_certificates(self):
        data = """

RequestID                  : 810
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : 3KEY\\nejaky.uzivatel
Request.SubmittedWhen      : 1/8/2024 4:56:32 PM
Request.CommonName         : signserver-ra-01
CertificateTemplate        : WebServer
SerialNumber               : 180000032a9a1aac7197589cef00000000032a
CertificateTemplateOid     : WebServer
RowId                      : 810
ConfigString               : vmi307469.3key.local\\Demo MS Sub CA
Table                      : Request
Properties                 : {[RequestID, 810], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], 
                             [Request.RequesterName, 3KEY\\nejaky.uzivatel]...}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_identified_certificates(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].certificate_template, "WebServer")
        self.assertEqual(templates[0].serial_number, "180000032a9a1aac7197589cef00000000032a")
        self.assertEqual(templates[0].config_string, "vmi307469.3key.local\\Demo MS Sub CA")

    def test_parse_authority_data(self):
        data = """

Name                 : Demo MS Sub CA
DisplayName          : Demo MS Sub CA
ComputerName         : vmi307469.3key.local
ConfigString         : vmi307469.3key.local\\Demo MS Sub CA
DistinguishedName    : CN=Demo MS Sub CA,CN=Enrollment Services,CN=Public Key
                       Services,CN=Services,CN=Configuration,DC=3key,DC=local
Type                 : Enterprise Subordinate CA
IsEnterprise         : True
IsRoot               : False
OperatingSystem      : Microsoft Windows Server 2016 Datacenter
IsAccessible         : True
RegistryOnline       : True
ServiceStatus        : Running
SetupStatus          : ServerInstall, ClientInstall, SecurityUpgraded, ServerIsUptoDate
Certificate          : [Subject]
                         O=3Key Company s.r.o., CN=Demo MS Sub CA

                       [Issuer]
                         O=3Key Company s.r.o., CN=Demo Root CA

                       [Serial Number]
                         656879DC6DFCC35C431488317DDB331F486A3847

                       [Not Before]
                         10/13/2019 8:33:12 AM

                       [Not After]
                         10/9/2034 8:33:12 AM

                       [Thumbprint]
                         66829B517CB2169DCB015988DA72DE6B7A7D75DA

BaseCRL              :
DeltaCRL             :
EnrollmentServiceURI :
EnrollmentEndpoints  : {https://vmi307469.3key.local/Demo%20MS%20Sub%20CA_CES_Kerberos/service.svc/CES}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_authority_data(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].name, "Demo MS Sub CA")
        self.assertEqual(templates[0].display_name, "Demo MS Sub CA")
        self.assertEqual(templates[0].computer_name, "vmi307469.3key.local")
        self.assertEqual(templates[0].config_string, "vmi307469.3key.local\\Demo MS Sub CA")
        self.assertEqual(templates[0].ca_type, "Enterprise Subordinate CA")
        self.assertEqual(templates[0].is_enterprise, True)
        self.assertEqual(templates[0].is_root, False)
        self.assertEqual(templates[0].is_accessible, True)
        self.assertEqual(templates[0].service_status, "Running")

    def test_parse_authority_data_2(self):
        data = """

Name                : TEST CA 02 Class B
DisplayName         : TEST CA 02 Class B
ComputerName        : ca.pki.local
ConfigString        : ca.pki.local\\TEST CA 02 Class B
DistinguishedName   : CN=TEST CA 02 Class B,CN=Enrollment Services,CN=Public Key Services,CN=Ser
                      vices,CN=Configuration,DC=pki,DC=local
Type                : Enterprise Subordinate CA
IsEnterprise        : True
IsRoot              : False
OperatingSystem     : Microsoft Windows Server 2019 Standard
IsAccessible        : True
RegistryOnline      : True
ServiceStatus       : Running
SetupStatus         : ServerInstall, SecurityUpgraded, ServerIsUptoDate
Certificate         : [Subject]
                        CN=TEST 02 Class B, OU=IT
                      
                      [Issuer]
                        CN=TEST Root CA, OU=IT
                      
                      [Serial Number]
                        5600000002B50D8D92CDA3907F000000000002
                      
                      [Not Before]
                        3. 10. 2023 11:59:59
                      
                      [Not After]
                        3. 10. 2029 12:09:59
                      
                      [Thumbprint]
                        04EE41322E5F2F3187AF13C40CA95B40BBA082FB
                      
EnrollmentEndpoints : {}

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_authority_data(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].name, "TEST CA 02 Class B")
        self.assertEqual(templates[0].display_name, "TEST CA 02 Class B")
        self.assertEqual(templates[0].computer_name, "ca.pki.local")
        self.assertEqual(templates[0].config_string, "ca.pki.local\\TEST CA 02 Class B")
        self.assertEqual(templates[0].ca_type, "Enterprise Subordinate CA")
        self.assertEqual(templates[0].is_enterprise, True)
        self.assertEqual(templates[0].is_root, False)
        self.assertEqual(templates[0].is_accessible, True)
        self.assertEqual(templates[0].service_status, "Running")

    def test_parse_authority_data_3(self):
        data = """

Name          : 3KEY-LAB-CA1
DisplayName   : 3KEY-LAB-CA1
ComputerName  : labca1.3key.local
ConfigString  : labca1.3key.local\\3KEY-LAB-CA1
Type          :
IsEnterprise  : False
IsRoot        : False
IsAccessible  : False
ServiceStatus :

        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_authority_data(result)
        self.assertEqual(len(templates), 1)
        self.assertEqual(templates[0].name, "3KEY-LAB-CA1")
        self.assertEqual(templates[0].display_name, "3KEY-LAB-CA1")
        self.assertEqual(templates[0].computer_name, "labca1.3key.local")
        self.assertEqual(templates[0].config_string, "labca1.3key.local\\3KEY-LAB-CA1")
        self.assertEqual(templates[0].ca_type, "")
        self.assertEqual(templates[0].is_enterprise, False)
        self.assertEqual(templates[0].is_root, False)
        self.assertEqual(templates[0].is_accessible, False)
        self.assertEqual(templates[0].service_status, "")

    def test_script_minify(self):
        result = minify_ps(IMPORT_FUNCTION_APPLY_FILTERS)
        print(result)
