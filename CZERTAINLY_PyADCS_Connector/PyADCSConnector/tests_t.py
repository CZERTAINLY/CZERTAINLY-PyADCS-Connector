import winrm
from django.test import TestCase

from PyADCSConnector.utils.dump_parser import DumpParser


class DumpParserTest(TestCase):
    def test_parse_certificates(self):
        data = """



RequestID                  : 1
Request.StatusCode         : 0
Request.DispositionMessage : 
Request.RequesterName      : PKIT\\TICA$
Request.SubmittedWhen      : 3. 10. 2023 10:11:26
Request.CommonName         : TEST Slovak Telekom Issuing CA 02 Class B
CertificateTemplate        : SubCA
RawCertificate             : MIIFIDCCBAigAwIBAgITVgAAAAK1DY2SzaOQfwAAAAAAAjANBgkqhkiG9w0BAQsF
                             ADBzMQswCQYDVQQGEwJTSzETMBEGA1UEBxMKQnJhdGlzbGF2YTEcMBoGA1UEChMT
                             U2xvdmFrIFRlbGVrb20gYS5zLjELMAkGA1UECxMCSVQxJDAiBgNVBAMTG1RFU1Qg
                             U2xvdmFrIFRlbGVrb20gUm9vdCBDQTAeFw0yMzEwMDMwOTU5NTlaFw0yOTEwMDMx
                             MDA5NTlaMIGBMQswCQYDVQQGEwJTSzETMBEGA1UEBxMKQnJhdGlzbGF2YTEcMBoG
                             A1UEChMTU2xvdmFrIFRlbGVrb20gYS5zLjELMAkGA1UECxMCSVQxMjAwBgNVBAMT
                             KVRFU1QgU2xvdmFrIFRlbGVrb20gSXNzdWluZyBDQSAwMiBDbGFzcyBCMIIBIjAN
                             BgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2ekTJSTt+npF5Wq2u1RXzQvcu6mk
                             6gbBZdsm+NuzeIy6WbAUI2sCObKvy1gcbBKh7cg5LYO93LRWR9OodZ8xwNN5R7V4
                             +RDNsxoEGcg+bi/+BYkuzvBbgdKvSVDjNyEfobxNmX0PqBbG1PcnL03kla6z+0+r
                             gIC2hosrDbBpWOrXwc0TuP4L4NfbSJEL6UlsoXZeNO/DT0dSTj2MASw8K66PnpnF
                             mK6hTip6RiCWf2Fin4nmuEam4+UA4SxwHcbC90Cgmsz5fEp2OMxxLaWiKUvfJUcg
                             fncp9YTBVOtN0KlV6Vu0N1rKl5yyiEz3A+6Z0yPrKmnb4YnnVaPQN9Sk9wIDAQAB
                             o4IBnDCCAZgwEAYJKwYBBAGCNxUBBAMCAQAwHQYDVR0OBBYEFFWwGZgnPofc3Bm6
                             uSt9K2qqcpEFMEAGA1UdIAQ5MDcwNQYMKwYBBAGClC0BAQIBMCUwIwYIKwYBBQUH
                             AgEWF2h0dHA6Ly9wa2kuc3Quc2svQ2xhc3NCMBkGCSsGAQQBgjcUAgQMHgoAUwB1
                             AGIAQwBBMAsGA1UdDwQEAwIBhjAPBgNVHRMBAf8EBTADAQH/MB8GA1UdIwQYMBaA
                             FGmCvkhlF7n0/sLd6nBaAEUmk/oqMF4GA1UdHwRXMFUwU6BRoE+GTWh0dHA6Ly9j
                             ZHAtdGVzdC5zdC5zay9yb290Y2EvQ2VydERhdGEvVEVTVCUyMFNsb3ZhayUyMFRl
                             bGVrb20lMjBSb290JTIwQ0EuY3JsMGkGCCsGAQUFBwEBBF0wWzBZBggrBgEFBQcw
                             AoZNaHR0cDovL2NkcC10ZXN0LnN0LnNrL3Jvb3RjYS9DZXJ0RGF0YS9URVNUJTIw
                             U2xvdmFrJTIwVGVsZWtvbSUyMFJvb3QlMjBDQS5jcnQwDQYJKoZIhvcNAQELBQAD
                             ggEBAJGZn81R3wtE5wSEXZra4rbX9APm1zcDXTcr99Zz+UHgVt9xm0z+X/vrsPMK
                             d3YKvl2RBonfMj5ytctngbPO7/Yd59hlJ9IqYCnSt01WjpaoPLdk3dxdmACTo5ws
                             eEgl71iimlv7nt9WnIRo3RsFy5BaZUpMopOUCZ9LGXNK3e7XqpsGAXriLLiA2G9K
                             PXuWlrgbEaiTLcMUuO9uKXFiN5E2rIVPSofpq2I/hBcnDQwyaZVRGK/ilWd5k1rH
                             ikbIXl8BcjvMUqe4cB8Lc765Q9AZyuT7m7/cvj1hVICW7itu0NWU61sVFliZcFjL
                             cID444yZEZ7olnlqvX3LM7A7sac=
                             
CertificateTemplateOid     : SubCA
RowId                      : 1
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 1], [Request.StatusCode, 0], [Request.DispositionMessage, ], [Request.RequesterName, PKIT\\TICA$]...}

RequestID                  : 2
Request.StatusCode         : 0
Request.DispositionMessage : 
Request.RequesterName      : PKIT\\TICA$
Request.SubmittedWhen      : 3. 10. 2023 10:11:26
Request.CommonName         : TEST Slovak Telekom Root CA
CertificateTemplate        : 
RawCertificate             : MIIDwTCCAqmgAwIBAgIQTdh2sin8J5pEiGo+be7caDANBgkqhkiG9w0BAQsFADBz
                             MQswCQYDVQQGEwJTSzETMBEGA1UEBxMKQnJhdGlzbGF2YTEcMBoGA1UEChMTU2xv
                             dmFrIFRlbGVrb20gYS5zLjELMAkGA1UECxMCSVQxJDAiBgNVBAMTG1RFU1QgU2xv
                             dmFrIFRlbGVrb20gUm9vdCBDQTAeFw0yMzEwMDMwODI2MzhaFw0zNTEwMDMwODM2
                             MzhaMHMxCzAJBgNVBAYTAlNLMRMwEQYDVQQHEwpCcmF0aXNsYXZhMRwwGgYDVQQK
                             ExNTbG92YWsgVGVsZWtvbSBhLnMuMQswCQYDVQQLEwJJVDEkMCIGA1UEAxMbVEVT
                             VCBTbG92YWsgVGVsZWtvbSBSb290IENBMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
                             MIIBCgKCAQEAzlBqGe+nmwEJBdIUUbEs2jHV9aX+KLQShGfsdkkiWdvvKqeKFqyq
                             Te/QF+YsOIm9KXqO/XSIQg4sCjeW+pFi3+njizykxH6rZY2FBJATW+Xqmp5zYWYc
                             +7Zc8phBKZ36UmTJusq5fbOWsJPXPS3R28pZncAgfWPq2XDbXqmTy6fgyxmjHlVY
                             MQabsbzJ49RAhwC0pYzNjj3/Ie2Y1mMzNfQ4zqOhJ6kigAlaKXZV41C8PbLg5nIq
                             s+qvAEP5HXUMrqBUdzppZeS1uV86xWflbF021XEOsaHRVBe2P75ArPW7vvciF/Hh
                             0foHHHu0H3HZ48r+1FvV+OQbbrwhLsDVnQIDAQABo1EwTzALBgNVHQ8EBAMCAYYw
                             DwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUaYK+SGUXufT+wt3qcFoARSaT+iow
                             EAYJKwYBBAGCNxUBBAMCAQAwDQYJKoZIhvcNAQELBQADggEBAF7IS3eRqQ1rY0ch
                             Migb/WLZ1HsZdNTKHj0uDYZa8VjGvq9OQKBFJtGoSwSCYlXdjrIsXk2p8n2BLuo8
                             KVU+DXj+iC67if9b5gHwlOGpuBp7Qw/lkMREKZ+VALY1RM2O/iTm8y8feUcHtzYv
                             qhgJt0k56ft7qViQOqJXLezTuardxeFNeH0GpIJGu6MjpkYe4r4H/Se6GJMCqxuT
                             CUKnbCK8P8xnjx0xZUIeGPcxrB/0vY8iFoy46GqkQMGnq2tJqGKIB9my1Qv1sSQB
                             AWM4Hk8nlSqPCPkI9wra4wJ4D7qoqJhlCUizaajFrwsm7UMojr7ORQ/5N+t3WUWv
                             NIsPdhU=
                             
RowId                      : 2
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 2], [Request.StatusCode, 0], [Request.DispositionMessage, ], [Request.RequesterName, PKIT\\TICA$]...}

RequestID                  : 3
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 3. 10. 2023 10:16:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAANAmCirElCKDQAAAAAAAzANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMDMx
                             MDA2MzhaFw0yMzEwMTcxMDA2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDeGTjn0PkT5k7YM9PF
                             CZ4KqT5C7n1XYAQ6nhGSrgb9VnCemdNg2tVIHL/WoLzgD3AWWj1MCe1Hva0btafe
                             OBxk3crvJJVdw/p4/wCjXjWCKUJp+zmIL8JIkWd4EQnKVO2evksAmmiPcSi65E6t
                             sXRr8hgzq/UhUcDWTcDbC+2KZeiXHtjE5rX9uT9tiYk02hW128/72/E7irGy0oGk
                             hA5T0EYH1vZKVt+IU0YMRlDDR7LZ07Xsx+DXgupmoXW7Us0FlVjomnKEUvyZJ+6j
                             eqy5/kzpFYwsnfCwxEsbmyBbQIskpM39vZytDr9Yj4bmH+qhQWHyVY3wj7iBRY3v
                             1DyhAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQU+5EkXoVBtTNnQoEmuk5Zl6excpYwGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQAQXqge5KcDqtdYCCKCjeOogQQxjJkdD34MUKMVzflt
                             ruQfv/RMKvt2z48beXO2D4ko/SbIrSOAwFoET/ofWEIHNkzVvmZ2hwE+z/gwf9GA
                             fkEibPCpKY2aZaNtknZQLWG+SM4isVNtld9E8ud5gvm8zb4OcnB1m9O4kU//OfeO
                             /ZXARb/IUdMxsogaZXWvr7yPrABABYtpVg4IKoUPPRBgE2p/m+h9FhZJp7+X8j4p
                             5iHgPPrAwmHrw4MxJqI+SeuDBHiw7htrwmZ/vqIgWACONN9JEdpqKXeEcBHmoQOC
                             ZigjqHkB1vhSYnuFK4fQDGldKxHQWxb1ePbCBjgaiSDX
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 3
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 3], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 5
Request.StatusCode         : 0
Request.DispositionMessage : Requested by PKIT\\mrublik00
Request.RequesterName      : PKIT\\TICA$
Request.SubmittedWhen      : 3. 10. 2023 10:20:52
Request.CommonName         : TEST Slovak Telekom Issuing CA 02 Class B-Xchg
CertificateTemplate        : CAExchange
RawCertificate             : MIIF3DCCBMSgAwIBAgITYAAAAAVnRGpwBHVb/gAAAAAABTANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMDMx
                             MDEwNTJaFw0yMzEwMTAxMDIwNTJaMIGGMQswCQYDVQQGEwJTSzETMBEGA1UEBxMK
                             QnJhdGlzbGF2YTEcMBoGA1UEChMTU2xvdmFrIFRlbGVrb20gYS5zLjELMAkGA1UE
                             CxMCSVQxNzA1BgNVBAMTLlRFU1QgU2xvdmFrIFRlbGVrb20gSXNzdWluZyBDQSAw
                             MiBDbGFzcyBCLVhjaGcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5
                             DldaVNjkiir762cFyhkWmJTIBHqbTUYOYfNPqMiBdWYb4PJQ7+DhoNsN2vihixgn
                             HZjyk9nRb2Copd1hvKllE07xPgzL2II/HaObcaXFsuUxACDzGY3fa/8PmsovM64F
                             J015mYmrQ0ouTFKYYzoiqGOziDuBDkgBOUkb7sPBU3+AnN4CIpzXtuzEJZcIjxV7
                             WpDUf0dCwJ9U8moqs/2HMJaoZo2gisnqBAxSz+Na3cGsgZskhNvdij5qtyjQsBog
                             s8rv83gWz1ALIn5RMgWMkBVEcNuoAx82gvF2Afnk6kDgloXFDv1U3A8jCrF0H12d
                             uyDHrSmYubWvL7IgCA1BAgMBAAGjggJEMIICQDAdBgNVHQ4EFgQUKE+S6AC4oG+t
                             +207zJqbCmlNIiswHwYDVR0jBBgwFoAUVbAZmCc+h9zcGbq5K30raqpykQUwcgYD
                             VR0fBGswaTBnoGWgY4ZhaHR0cDovL2NkcC10ZXN0LnN0LnNrL2NsYXNzYi9DZXJ0
                             RGF0YS9URVNUJTIwU2xvdmFrJTIwVGVsZWtvbSUyMElzc3VpbmclMjBDQSUyMDAy
                             JTIwQ2xhc3MlMjBCLmNybDCBpwYIKwYBBQUHAQEEgZowgZcwJgYIKwYBBQUHMAGG
                             Gmh0dHA6Ly9jZHAtdGVzdC5zdC5zay9vY3NwMG0GCCsGAQUFBzAChmFodHRwOi8v
                             Y2RwLXRlc3Quc3Quc2svY2xhc3NiL0NlcnREYXRhL1RFU1QlMjBTbG92YWslMjBU
                             ZWxla29tJTIwSXNzdWluZyUyMENBJTIwMDIlMjBDbGFzcyUyMEIuY3J0MCMGCSsG
                             AQQBgjcUAgQWHhQAQwBBAEUAeABjAGgAYQBuAGcAZTBABgNVHSAEOTA3MDUGDCsG
                             AQQBgpQtAQECATAlMCMGCCsGAQUFBwIBFhdodHRwOi8vcGtpLnN0LnNrL0NsYXNz
                             QjA1BgkrBgEEAYI3FQcEKDAmBh4rBgEEAYI3FQj/+l+C4uoch82bJ4erpkGDkmI0
                             ARoCAWoCAQAwFAYDVR0lBA0wCwYJKwYBBAGCNxUFMA4GA1UdDwEB/wQEAwIFIDAc
                             BgkrBgEEAYI3FQoEDzANMAsGCSsGAQQBgjcVBTANBgkqhkiG9w0BAQsFAAOCAQEA
                             V+kYXXJYqiWvLfTcqs87TcGw2VrHt2FCFTzBqvPl2um+HIGGmr7yY9WTsVFRcS19
                             0gxoaEOA9HzVclAcbnO7rh3ozu3B/LMazsdmRYdS/WKPRsnrInefPy7Cpf2wX9Nx
                             HYzLRQkOhlWkKo4Qcf9UxRM3lHGPuDgwwGSvaGPH22pI2f6LnSX4+ft9o3rJqEpp
                             Rlkua9BIxK8QRY6kNuVw5a3g7x764VCVmfIqGSLH6FmJGkDOfRHQfN5HIpke3hRC
                             gppZ+TF50mRRlJDGkiV/ET02gQ5G0pKBph2ePq74EGddnmteCVISarPrHRonENLi
                             BOnmmWmdWXxIA2lF8Yuv6w==
                             
CertificateTemplateOid     : CAExchange
RowId                      : 5
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 5], [Request.StatusCode, 0], [Request.DispositionMessage, Requested by PKIT\\mrublik00], [Request.RequesterName, PKIT\\TICA$]...}

RequestID                  : 6
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TDC00$
Request.SubmittedWhen      : 3. 10. 2023 10:24:46
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.12632262.7838408
RawCertificate             : MIIFrTCCBJWgAwIBAgITYAAAAAaoHEwPieWBrwAAAAAABjANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMDMx
                             MDE0NDZaFw0yNjEwMDIxMDE0NDZaMAAwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw
                             ggEKAoIBAQCsJGwbpGDLR05y/QP6ZcTTrPEBFoXt2h2VGj7Eg0tbR67BQx0+VAGd
                             fenJ/vE9AcYuF6bOcwpKMSxK8NlXLG7w532hqN2U2vfnb6/gadLZoVAaSNZ25gs5
                             XCLltTeka/wvfSLVc7CYLRKezzKVThIMfPHvyQfkgeefQpd7u3+FryjVn6IX+Xgu
                             6vUHU2jPlRPqjsUEz5QnErKkeewDXcICC97VELUMrb6a7HVC+RWAqvaXITGjTDKb
                             pMkXuvClr/0uRPEOrOke1px5v9yXRtnueK4a01h+Oo7dGpbL+5UZ5uUxKW40UsEU
                             xsXTIhfyrFbT7zLC7t85YinUDRtu3VihAgMBAAGjggKcMIICmDA7BgkrBgEEAYI3
                             FQcELjAsBiQrBgEEAYI3FQj/+l+C4uoch82bJ4erpkGDkmI0hoOBRoPetUgCAWQC
                             AQEwKQYDVR0lBCIwIAYKKwYBBAGCNxQCAgYIKwYBBQUHAwEGCCsGAQUFBwMCMA4G
                             A1UdDwEB/wQEAwIFoDAZBgNVHSAEEjAQMA4GDCsGAQQBgpQtAQECATA1BgkrBgEE
                             AYI3FQoEKDAmMAwGCisGAQQBgjcUAgIwCgYIKwYBBQUHAwEwCgYIKwYBBQUHAwIw
                             HQYDVR0OBBYEFMDVeJyJmcqUmSsv56JtWRa7juouMB8GA1UdIwQYMBaAFFWwGZgn
                             Pofc3Bm6uSt9K2qqcpEFMHIGA1UdHwRrMGkwZ6BloGOGYWh0dHA6Ly9jZHAtdGVz
                             dC5zdC5zay9jbGFzc2IvQ2VydERhdGEvVEVTVCUyMFNsb3ZhayUyMFRlbGVrb20l
                             MjBJc3N1aW5nJTIwQ0ElMjAwMiUyMENsYXNzJTIwQi5jcmwwgacGCCsGAQUFBwEB
                             BIGaMIGXMCYGCCsGAQUFBzABhhpodHRwOi8vY2RwLXRlc3Quc3Quc2svb2NzcDBt
                             BggrBgEFBQcwAoZhaHR0cDovL2NkcC10ZXN0LnN0LnNrL2NsYXNzYi9DZXJ0RGF0
                             YS9URVNUJTIwU2xvdmFrJTIwVGVsZWtvbSUyMElzc3VpbmclMjBDQSUyMDAyJTIw
                             Q2xhc3MlMjBCLmNydDAeBgNVHREBAf8EFDASghB0ZGMwMC5wa2l0LmxvY2FsME4G
                             CSsGAQQBgjcZAgRBMD+gPQYKKwYBBAGCNxkCAaAvBC1TLTEtNS0yMS0xMDQyMDk1
                             MDM2LTM2ODIzMDgzNS0zODQxMjUzMDg5LTEwMDAwDQYJKoZIhvcNAQELBQADggEB
                             AJpI3X9vNuM2Ei8Q43jxbx2BEAhO6Oq7KTpUcgabwCD66FD3uiCprauRgXqLBeOb
                             yJQwBzWpyoFuNqq/SuXdDxrMOKuQSmP8avBvVEIbSpdd50Wzw1lr8jkKQR8sAlf0
                             UdV54hd8yTAVd/bDBWKTu4rzkm+ws4/75JrqrlwCXwsDBJFwboMtcr+g8ia9VwFB
                             /rFSvWl9zaDOsOJ5CTTD/apmSf/CmcN++kIm0M8qRuRKaKvr4lKGGhmXkXZKKkg1
                             FP9GyFHjFi4vO/OYd6PV5rX2Lad9MyCuINXfToCCwCXLg60iGG9FgQd80VQV2vWB
                             +YNJdEh08QLEsvtlkKVH+q8=
                             
CertificateTemplateOid     : PKIT Domain Controller Authentication (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.12632262.7838408)
RowId                      : 6
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 6], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TDC00$]...}

RequestID                  : 7
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 3. 10. 2023 10:49:48
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAAeQBm3DBvTZmAAAAAAABzANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMDMx
                             MDM5NDhaFw0yMzEwMTcxMDM5NDhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDW6fKy5Kam6igOIGit
                             6+3C58kbErOJt4kJcv5qyAKTnRdG7A4E4FG7YtcnzWU0qITWoupywkBcQbqc82jh
                             nIvVyRXDNXxGVwlkD+CsHQxP4oxQtYX5VBPCuUUOSvgbyRRjsAA7A4bwbJ2S4BjX
                             RdOSKuM/yci+pJUrtgnwijt4TMMQe6fq63HY7Mk6nuu6gJayEV8C4Zsn6faQglRs
                             YYmAoC5lKnoE/mQMmgueX20DT8Jcl+jLg8RXe4945wGpTKzjuQ44Pa15EpAlvppb
                             lTzLApjQC95A0RocJtyE7d4SU9eTxUzYIX2iKdwnxtRC3sg09+AQgO9gAW0qN9Y/
                             S0cFAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAdBgNVHQ4EFgQUbi9zlPnEc5Xv7ZnRYLDho8S7FRQw
                             HwYDVR0jBBgwFoAUVbAZmCc+h9zcGbq5K30raqpykQUwGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQBJNmoCWFbszNp8snCs4m0c1b4tgf74mBNRsMagbHMA
                             iRKL/smEC1wW1+apA/gtVAmU6zFvyODFfBCjK3Thj+PO1LreUL5DGuVl/x4gMRHZ
                             CncdmhpYrxCUWp6NKPqv+U7XoWGRIBQGRqfS/pZ7rawCewmUWl6qoRSRYVNkU6Cj
                             RfQ9KmLPJx8bkYhHK+zNgAz9PP3XcYuK6bmM6LoNqa4JNSk/K56aMuNEIZrcAU68
                             DFS7Y67JfSHAWRPtmELLLnyOcTzgCrd68djiGFoC44hX/jC/GrXHmwd5Q4Y2Nme2
                             T2O2IjiywC19Nfn7+p5va8ibFsYeCmDGoOy6HC/7CFWY
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 7
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 7], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 8
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 15. 10. 2023 10:06:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAAjoP+3TXIlgjQAAAAAACDANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMTUw
                             OTU2MzhaFw0yMzEwMjkwOTU2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCfddOZP3cg5o+59EtM
                             RZpKrT6O6nFdiTiZ31FE9A9nn4HJHWnoWXXdPouXQZvSeNo57pkY5xdqLFn+OX3L
                             Rv0qIwGlCd3cxUSQ8LzzbEN5LKhEwpukU9hKUz80NAptto2D5B9Td8RjQb371Rd6
                             MUsoatiEpHJkOTu6v8IHD3k/tqouHdaELeRqHVrurPM8Ki18j39rEo9VS34K1Vbg
                             mFHEnqlJnYl58PZaYy/ABy2pVusJzgvtp3N+OURYh15rRAz0IamqX5gS0zHhx3F6
                             4V+mTLl5/ZJJ7zE0lM7Isq5IkF6YNJVOjUedD08ohGCUu0R9aXBNjBdfKOD1ohnr
                             ryqJAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUFWmQiuLFwv6ZUiwzt1S8Zy/z6iMwGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQCGzqFNDcOqnlQ/VfouOf+m2CbIfC7YAjpAmdVI7sY/
                             qnUXIKOwZwsQsmO8Bz0QURcpyjeRpZ1+Ba9k3i37HXHswF3ZlBKKXca/FStR9X3n
                             VKLErociGWpzwpPclrvXpol1eS/J+thDuGgnuUm9hRUEMOy7qOL4KYTbnvfZ6qyY
                             k5xp/y8ytjDjOXzvNs49vvQCNrYExbgB2eQqIfgH16O8I8fKVYwbRcJ1GBvvKGP/
                             LX6W1zVdUOrm4Oiv8OPJ9uvNoUiWImOws37dCrbC711jyEYGG6YEEVBXa1dY+KRd
                             HRX8+x65aMri3vokVcQ9M/qoJwGRlv3C27kCQEM4GW64
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 8
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 8], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 9
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 15. 10. 2023 16:00:01
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAAm6DlYVt8mGEgAAAAAACTANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMTUx
                             NTUwMDFaFw0yMzEwMjkxNTUwMDFaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCzDl9dLIt54Z0FpF8o
                             misFHIG/VuON5vaUZu9J5FEiwgpCS7dWsqmQbe7Usrcf+UsSZHSj5EnRR4mKLUVT
                             8QX4OnX/57VaqdLZX8OywNK8Tx16vd6PZVld6X0o0+Al7D/lWOCsFAskvZIImPOK
                             lNf+kqScg9zCvoxo6wo1FJiQl7SV0/DQNhsMppWk/pP7TbgU7PevORNGmcOWhG0f
                             fndv8L3VuJhmtxtQbjOpspPLsGEu7eh3zNoZU11OB1U79/rGTF7pkR+9e2FUxZED
                             CcSpTvTMBWqoWE2mx7z4CJJoKL7jwUifZr9T0qPynLj1ml6creYKt7ZzUFYJgOW2
                             f2FtAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFDEwaZ93uHom
                             RoQDz4XM6OnKCm/hMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQAG1qNcCGLlReD6VmotWYaoxSj8wCjnu9AbinaLb57h
                             rcydwArBocakO/yGMMjYg5whMDuhU6L4zy57Ffw6IKqQi/KbLHBCnGKJru26w6X+
                             pbtr/8brEAXviDQm8UvtCKtQEg6Li161Wbf0/c3tcJO9PS0Ebzv3jA5yASj7QQY4
                             ZcOy3uZddP6S51wR9BuDQeGID5xn9SOluVYzSgiADWPxpiqluqv32jYg8wPjxI5M
                             fqznT0Oy+tPdzUCsds9Y88wAjRaq9EuXRBKR7twemIdatf63BNlxcRRlnrWP5GVT
                             nEYLWLLe1/QrZ2Pj1Z3e4ldQLctYqjJ4kGzxoa3K4lkw
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 9
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 9], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 10
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 27. 10. 2023 9:56:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAApEDS+v+pIvDQAAAAAACjANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMjcw
                             OTQ2MzhaFw0yMzExMTAwOTQ2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDO6BVuvkW7fdDlYoWq
                             JraYwf8PXLbySy9xP1s9MiBNXOM3CqNUct836sszhFmPalDLI//tDr+ShTJOsAJ2
                             WWAla41ZnlldX73x5XRkCgMMUCJtFJCmeC3THTEktxFh2RUz6glShzarr2jnVGYU
                             d5761/76OFU0GItxf+6a1Pq7OiWA5Yg0RJj5t6OGLMh/q4ViN/xQhY3CELGN9OKZ
                             t09J0hOXVUd6r1KLFKDaZ5q6ACwaG2/efq2ePj3S7ldW59g/w5MrU/Qs0+eVg8RA
                             d7gN4VtnRccTSYo1LynTG9IcDY/1yFcx1g8Ft+dqMT5R4Wg8VO9zoktcKHIIYoVM
                             IE39AgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUCsLFoVjwjVByJYH0AVGd2nJgn48wGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQAbGjFwlDS9/PFBVJJJfBjyGDx3UY4C2td0HDpNNnHj
                             0HRHsMOPPioT4wHbsXqSF2JVAo54tag/r1BLXFqvOQBMXagTbBto5RM3aD00KPWd
                             PWFFjb/0y6tRrWrU39naLQk+rbXxVoipYYeTWOMdLOYb9We6VOfDF05K63ihowzw
                             hcyI8u4WauMg1toSXp8tn9BMlBtxNGqCILN+u7DmXSZfGekHnJEYG6kgRgwbuYF8
                             kmIVZNksP9iyGnoA+Rj6uUEH+NX/wUqkQNSEpIvlqQlkz1ILfgImKluz2kA+xVRI
                             B7GPW86oNdFO2I1hST1VKUpmcQdv58T/ikfmXh4Igsjl
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 10
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 10], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 11
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 27. 10. 2023 16:00:00
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAAv+fPqXptIlHAAAAAAACzANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMjcx
                             NTUwMDBaFw0yMzExMTAxNTUwMDBaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDCrloxzrQeppPUgsSf
                             ed1BJ+hmjo6dXajjGfdYEBV6UQewzC7sCgqdFeDJYDxaYbCHSF+F5IhZRX5trWBc
                             KszKYeNUYsUf93mx5nuK46pL7dABQ5gPGL+FFJlcCjN2e3/UJ6lC6OP4SkUt/tUK
                             bCmHarMBf/TY04yHxsD28u4Anf7dFGAfr+PvcWre/q721mVXgmPeFeM2W5vDMQLr
                             fWYpOJ5le/jHhaw8PkX9WO+Ng5pyOXVyscab+ukBZpVDmv53uiXlNm2bhQLw8qD6
                             ++4cNDJeNbIGZzECdKfwG+EVnSJWkNgFOCizZI+VNneYHNMwf0lNjiyx0C/MdYyB
                             mRadAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFJXgUd17tHBJ
                             pSuswLrU0SufJfqDMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQCkbX4FIf1nrjiiIa9qvcXCdIyAdO2O0vI+Dee9F/im
                             6ZNMLN7BggLhDT1TljcldJgXXTLSs4EB0kOc88nZMArPZI8eiTfhFmRlEhqD7JBB
                             Boy7SNttBlEPNPWNZvK8fZkCJuoWVWAOSaqs5Bxp06Z7HMsy0XsBeLzciNh1FUJc
                             3ZfdPsSxRmjNQkJ/kqMXshwstBVrzjFyi5fi93v7LiArryGoxuFKNxFjiXycyIKG
                             3CO02mB5sCo/aiGuOym356r2PpSsdyZlC2AYJmxjteXEDKj4x336bAjwJnspNJK7
                             BWhPa+GbFnz8kvbMeRoJHxan1wYq/mpoDtlZ5wV7QW9t
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 11
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 11], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 12
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 8. 11. 2023 9:46:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAAwXPxEBfqw4IwAAAAAADDANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzExMDgw
                             OTM2MzhaFw0yMzExMjIwOTM2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQChnmstYwIj1KxDhOy6
                             mvaeWmxz86ATDfRZvw1pDo4HgqEW+B+qmqa0r6KcjeYtV5PW/JbW+iSnXHzjEM8z
                             OANOMisCQJO6ysmEQzoQzH/xf64tLGdkYwc2jNtFt3SJdgHN2aIoAeodVJ4xffcd
                             YYCqc2SFMvoB6/prsgiufgDSHcyvKml+zrvJtOUuT52huejlktXeWfWme4ejh3aW
                             JSqLWBlLkSbM2XtkLLGGHWeekN5Jnmc9/UjC5/JSvxPEuKwGwF1AN85PzYqAj559
                             D+jd5SZ0qp76AjPmaGPhKU+wNVuZ7mGH98ymK4MfOfEEwxY6sKmxx78MD/eS+BdL
                             E4/5AgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUyfzl5P5R7I6qNLKkkyHxkcoqfnIwGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQBNz+iYY+L6MM/oKHs0wjEt25sNEBhVq9MM1VVmMrS3
                             XOt12fpyAwTjP52x33HkkVb4e1uNCVuF4S3pK9l149xPON9/enjSY3NFEv6aO9IU
                             TXj4n1m8cs+tSGE3ZhEhhEv2tAevuRHH0d1EHfuT+4k7lVEl2QAlwUep/nD7NVWk
                             F0wI6MIeYlADMNuWzotrdqPBW8TuZy9MiWDyVkSKg7Q+99la9AeaeDrzYW28C/Jq
                             qjpnzZ6w0ST4b/jDEJ6naQgd+jg50Zb0VVyBDq5AA3I6gPfc4rcLcH7mhroxhc6z
                             RIlEZkPQl1E+2xuqaa13h0J6iD6jsiDmrHSBVwRgnVhZ
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 12
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 12], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 13
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 8. 11. 2023 16:00:00
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAAA1ETF0ebIA2PwAAAAAADTANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzExMDgx
                             NTUwMDBaFw0yMzExMjIxNTUwMDBaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC8NkOFHfJLRLrMJpqF
                             YsW7Tx6zW1BKVqPYGKYJefsjsG/WKtFOCSuoVh1fnIcTsAt54RVToqjg9WG84S9v
                             TqkYgernoZgpqAJuDzsjHfGrQnbJLrrdBuDyPBa3YY39CX9CE1JLpNxVJsc7vrv6
                             GwDNv4CJsfi2f5ilPbnzXzEfqq9GJLWD5gDwho/h951dnE98Hi0R0baJnpEjJfId
                             62vzMCsaTUVzt2414MMl3ku4IJE/NmJb+eNEikmdcM+VuO19FHMk/LYtJZsbGggF
                             jGxfmekZVm75RduxsDpKUPFkEzrp4Yvzyb3S/LGa6qiv+MiF8EwD5RRlXysmcfTS
                             SdnlAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFF4h1ML217gq
                             Wkc9YzZQ39k6r66xMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQBPZcDPgaaPaMm+9fKXsrS6HazNZDKKMsOub8DynRuB
                             6KSlFd2/7YTTbEelQJ7Tk5pqjkwCvmDISTqu8BuYd/i0jKJWdDyxREBaYAl4SMYj
                             UMlvoJwRHLKXOn8PlK2hVfN3Fk0X+f0u6W2Gtr+S4eZ/Mbz1ojmkYjQfTNmkNt5I
                             acIIYKjXhEyVEVX0chtPGdKnWHQ6q2i4qd7x8Hzs66UiMv7YZyrbhoMsSdMIClxb
                             qYfo6/ROSHAn5Grfr/xWZpR5DSB9qQIJzchDdmXSWt+nS/HYBVbBp8QihqEsiWV0
                             /zvjV+l+6pPBD2Ac5Ar3OCAKOQbyl/EDNKV2e4bD71Sv
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 13
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 13], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 16
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 20. 11. 2023 9:36:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABCHnHi2Voe4tAAAAAAAEDANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzExMjAw
                             OTI2MzhaFw0yMzEyMDQwOTI2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDPU9S4IRAdolpzak64
                             iSNigB1H0uRsPFRG/DnwdTENCeGAYcj/Q8Ub9bYVFrRTa0xuiegOHpReHxdFJxEK
                             M5cH57jrBrbapRA9060FoNpa4PMuD92A4TsvV4U7cexZbptH1b0d3Tzgb3fUowg1
                             0q4HzW4ULtKB3cmdai10f2Mgw7tUP2TLo+aSgS6wfydQ/8SsqhtvxPEz6hP1nt+f
                             eA5DDLSP3JEiWlJVnqsZSl274ERV/MbXYnRYA3ChoxpETWu48JO8V7hxy3IvLfnT
                             ko8Rvzi4lJXwJ2hIHPkSu/LJ+veXvHjzOp2Rt5oY/G7WBbQuqy2pMqzppU4xZgmJ
                             lajxAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUE8t7QQ/NdZ2/Axzuu/Ao/eqcXuswGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQBey7J1CCBQhdSvrklws5vSGhhJqoaAhRRM1XrpXpMx
                             tvTveT8kngEYIzQt4HuI+DMq1bgqtNysjaMeb7vbKsJFIVYglucDvjcU8hL0WxrP
                             cpLNuwRi7Sl9fcFbK2ZQNujHOzGM5S3+YIyOMqtlv/LaylLMNefln/FbyrxnWjxf
                             NtOlR3tssM4UoJjuJzeyHHy8XCTLApk/1zJKS4PikmOUIEeE8xeWQvqe/OGPIegc
                             t6G00+dHcxPRgG/frJDVecVWvvpKjP96L0NTprUPJtVSQlpIEg4XN/LG8BBl2Uiq
                             5N/yV5vYCCj3gE1P2tTd74Xt4gXJUZOUplmQWRcHIJHD
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 16
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 16], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 17
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 20. 11. 2023 16:00:00
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABHlxXlMehxd2AAAAAAAETANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzExMjAx
                             NTUwMDBaFw0yMzEyMDQxNTUwMDBaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDt7jfMt2a3CC8fJWJ+
                             Dp/8UWLPLPW/wMgiINNfdfROx7tvo8Qx+/0ckGfsH5mWJVwLYaDGpRFCJszeN4lH
                             AVc1zmuwDa4KrsgwuebkX0r3wHPdzuNk70ZRVK14BismlTX2nXFzrD3z9sMUGJA2
                             KmeLQEPCpP4yXBSU3gjx1KjkR1Ed79+xvEyJCZaRwmF5botQYJ+LWE9DqxfDIECS
                             mT94WiaU+ZTdH1ArJClm0Mrn6dyqjEYJTA8IwyjWtMRs00gFNbUQxOGbA1pMf6RR
                             kmlaAff04dXWEr6K5RC8LoildFo1RcTwfR6r7xCLaj76zoRFZB+rdmfkMRedKhIq
                             Nr7lAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFCq+J4qcclcq
                             /9e2wbR/bxfB8GcPMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQDZHD4HwipwLSkM/RnRBc3Al+ASA//mTR6g1TCUiEfk
                             AszEsM7vJczxLYyJEPtUgD/6JCnZWUI7McOabLw5E/vVoqTd4Yz0myLaNdlEgyAh
                             bEGG+sZCL+DOCH2lcv6bb8Njo97e0dET53BS61YQlt+7p4d8V8LGbKq7kVweGB9N
                             40f9B4wyyQT6Ucwq64wYFJudoe9fdBGuoja9+ym+9Pn2o8RdYXnDBZZ93p5SFhOG
                             rza57xxvqPc6nPVhHlyXw5TdNkt0bIHQ+s0uWwwo7DGeychVQZgQ6ovahIrhkXWH
                             37vgw78YDSnZsU5qoE7oBuEx25CJlQkjbGyJGCymwpdm
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 17
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 17], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 18
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 2. 12. 2023 9:26:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABKItPV6BM53sQAAAAAAEjANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEyMDIw
                             OTE2MzhaFw0yMzEyMTYwOTE2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCWGekVPNdt1NIFsldo
                             N9mY0rJAIAXFEjMYb5vu7fQUFIbXGKr+V6UPsRODbIqmcnmOirB9GF/Z9ighzNAZ
                             jQTxYIiy+WX2u/YY7zOvNSS3+gJvK3ehtPXBt1XpvI+c4mMy4wa+pKgtnC4BPmGZ
                             FI9ZJDFPe4NlNTQUlKQltAhiH7L9z4B4hAWBNg9p4hABBYVcYalcqJOUabvXCAzs
                             zQbDVs4sOkkkEBEuC2E6s/wijIiSA17UobGyXPAyHcvuJvTbt2WckCXvxgAlryup
                             45oGTY2H0ZnE64Wvaj1K8LApiLXdeh6+jB1KeQWlAJHsDZGp5xthLiQZo8Al9y1G
                             2Cv9AgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUf0w1mx6ozwABTQz8HNzD9ZObyK0wGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQBG/mq1UB8wqunx2QPxKhYuCxXvSuOlKTGdf00+HpHj
                             B3SpPRr7NREyWgNH+R0Nxr5E65NRAttjXbG/ZaI89QIhq9/lzWAeeFoG1PlTx17p
                             Rvyqr0ZuZiCjj9O8I7PuF2JrO27iBxOCAw9k5DdGtgWQVlGE7gi0B+BQRP+dPI7Z
                             XHldpQg7S5M53zkcf3ttl1WEYH9bU+Ljc5Zdxr0bu7yjFVQC0pwkeGCZVSx69JjK
                             n4FatAsx76I6uf3CAgj7dT6nVpQR4xUdHkncOq+LJgbNZ+fQJ4iqSVnU0Q1KenwK
                             rXi3d0lIPw7wqbpMQJ1DuyHrmOJuslnGVUsVVgeupL5a
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 18
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 18], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 19
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 2. 12. 2023 16:00:01
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABPyuHQ7ED8V+QAAAAAAEzANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEyMDIx
                             NTUwMDFaFw0yMzEyMTYxNTUwMDFaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCrjFk0THmffUS5jaLr
                             ZJ8FXm38MDnYofBGyhY0M+WZiMP6aIsnLc4MN2HyDBKDXnDQ3acTe6r0l5G4kKJu
                             YewKiWkDY2UgSl+1iLWGt1HWKN+6Oiq/MjFD21KZ9siAq643yAsKo+UjoxQDv9Gg
                             aVrtCKRxg2/1f9kHpz7+8jpCJKpwmNPkmEyg6nw6dBFXDE6otQX2+00wmNynOR1s
                             8LJk25KvxbnSxN8YUs5D6ddx4S7d4OSDaVM6nQcyAkxTOieqFw5sbqZ8WyibhCBu
                             OVL2XIAgVO1TcWQsMdP8i94nMSVkCyEVWhwGU4ix6f/Q2RSDiU0RMwfZwYolTcgO
                             sQc1AgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFC8rP6YFpJe6
                             oHLZ1SYJwsgNnj4eMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQCkIrxbAntPrPsP0tVes6gb4zv37miCYly92Mf87SuD
                             XcBaKlQFIG3k6i6CP0O6ZAqNbOjTLt0ha/mQA/fcO1i6ySILDB04wHQv044P3tqK
                             JEftAoxs1SAWv9NgLndkc6MDqun4Kzm0KIBRbRAF4EgQkFmcPcjkN7k2EvUhpBD5
                             zYy8RinacQbFe1wbtasLsfd+f7qyMaxc3sGSsTPygTprMDg7rIUHBMqgCzQi28P0
                             9N6EdleGB/uH6YA47nWbcsgBg/spQwqiJZvIjxiPVAfcQ4xnJNu3Fc+KHR1d71PY
                             xcB0gLfzrMHLVo0uE6l37qXBdTZmk5ZO7qA1FG10AUV4
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 19
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 19], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 20
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 14. 12. 2023 9:16:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABQl/GcmnlXkZQAAAAAAFDANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEyMTQw
                             OTA2MzhaFw0yMzEyMjgwOTA2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCxNH3VfBXGs5GLrnOY
                             ESQ4EgNp9WBQx602TPHMdWFnr9g8eyT7i9c8F+bD8+X7dmaN2Nh2ZwB65owfjDH/
                             vYyMGidhPFiPmk9WbWia80RP0Ts+ptqnNrIta6izuiGlOZClO57IDqeLKEIW6itQ
                             bboljFJSjaWPN6fbtUtbrGVnw5zTD3ZkPNG7UT20haLgP873JJxhKQ1Tmvkss1pI
                             8wJZXi5vfxZC0cYq8z8VOTjNp/a32i9HLVLfaJixg0Q2THF+o70kbyliLEvnZWhk
                             MRElTgGWzTyLJTKxjY0zxW8h8OzrwfVVhY3DEcixyQSfCTWe1LytpEbA+6iNFbd8
                             rYaFAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUJqObTmurBxJyILcV72Z8nmOVaEYwGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQA2Q+PUkwFfYxECqTB5f4ZSOBwMASkjJssiN5F1Td54
                             lGRfgl6OXWYw+DzQeijHysfCM23YK99UoIKi2W92Wy09XDr9LNxJ6tmNyj98vF8Q
                             v1AX+WrNjujvJ2CmpJ9asf6wtCc7z3RCwcgw1Yz0IK4Kwi/MNUoXsUMtDZgJbd/J
                             O0gu7xiNQOpTBbP+sGOUeY2/Q4NDI8UbIQfh+J5UlBv5ElDAg8e+YLsTG0556zJV
                             CqQLFJQNLrXISLoxf3NBvX76qEeo9tJbbi7hE1KyPoLJCBDIdNnQO87YMP6KILCt
                             pFnXUFRTPySW84HuWiYgxZU8M/DOh2DSYikfHrt2XkRR
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 20
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 20], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 21
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 14. 12. 2023 16:00:01
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABUHSSbAgVC6IQAAAAAAFTANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEyMTQx
                             NTUwMDFaFw0yMzEyMjgxNTUwMDFaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDgcGKYxJif+/oHpnRx
                             /lv2fJ4chpu2YyKh1WpS6bPZpBtrMlPWTH1V7+/al7iuXkZ+0GZHbJPBDUNC1nZO
                             XiXTkQ64zBolSQBe8OpKjBQtGBjacr78FZvNM+dDPGSOjlY51KIiZU5jEpY326IK
                             abw0yVv07okAVor+XG5ihd9hvJnpAHDFYaot5tbwVnOyWes8o55Q+L9VxzdJsFua
                             hFHyOrEW37JvMUL+qxeDhjK1oRm2KU5348tUbYMY6lSJdHoHyVSgzQbzuQt/2Qg6
                             1IKJtLmWaS01RiwtdGL2uoW4t9XY6PW7qpIpf3YvtJdKyxZXwOYoEgG40jM7e4jz
                             cIMtAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFA9BSvntQniM
                             JkJzLbeL5jDmjXtIMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQA5XGPuDNOB9ceGbqWrvmLxzzzP0pxUqTY5Z0McLOOP
                             K1OfjxY1Uhgz1VYC8jI9+XMO4bkO2fzrVAnmLsMqnNI6E7eMDfNbJmnUtFJDkRnI
                             yLQcEM2zQdfBrQC8Oi9DCGKMQwpWK4skgNjblepzIQUe5/xCgmBJJpUB0Va8EDxE
                             F9epOIJO9hMFiguZo2K+9raV1GjEi0FcrLiNhU4mpFDsVy6OWcgxS33zYJMrvXiX
                             Ugx5fqK4/FHz3P4wePB7LEfxZVb7xZcK+BQsHqJECwBrmVm275GcPEwNXzIhMuns
                             prl00ZWLJ/SzVnEfIhSu2Eas6e//bFFqkzzx8oFt3ifs
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 21
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 21], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 22
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 26. 12. 2023 9:06:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABZgZ8TgJQkxJQAAAAAAFjANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEyMjYw
                             ODU2MzhaFw0yNDAxMDkwODU2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC5CVU+dB+8ee85qXaY
                             7McyuW403yzs4ldcdgXVsYwBscs7EOdBQsxdsA4cPX23Uvv19xFQBmeKyr7KN4zc
                             pFjIsXH+eEbQJhe9IWwHCUwNVKpyOQRqwW6xWP1qlSUXydH7ZbqOQPPx6lgG7J0z
                             op2LnXdtTN7npBnUqrt8htdK0vI7ijFrz1c3mFdV0FaPpAXWnY4683FkNz3tLTmn
                             qpoRregDRmlex3UyA8owsQrQ1CN27ucYZeAFrE2dOc7/vtPIAnYawwgI3aPDMuRF
                             v5YmzJ3n2D9wjYIvKRlgpSNFxU1bzUNOhHsxOeQSfJDzBZnrB464l8u7i7UVGnY6
                             BdqNAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUi/8sb1HCo4HKfV3mYWijAJ0nizswGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQBv9pd/q06lZDqQmEev1XoLqRfxGWF/gELggwfYEYfI
                             wonz7olg0/65v/7V9d1Y04iIIVxb78hoRTulGxhRTp/WYMlgLbqwkp8hFgaq+gWm
                             yyJijxr2JGnaYzJyBVbzDkAyiGlgV0zuJu4TC2EOmBf/6MDCobXzr6EO+rYS4T0B
                             JA4iS4UuE7ovZo9ojJPuik8SImX+ArsthVZ/NcVB8FaWz8S7L1sMI7wPdsXqYOZA
                             d9nv6sS47NlvziTRXkGjzuuBOH32uN+6/ZInqJt+xogHO/XggGno85uLtKbmjE4e
                             hoVRTkR1mT/FkdyM/ga4/kBYE5+if0H8PzZBpFV6r+mQ
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 22
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 22], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 23
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 26. 12. 2023 16:00:01
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABf66j+oAmy9mgAAAAAAFzANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEyMjYx
                             NTUwMDFaFw0yNDAxMDkxNTUwMDFaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDmk/VLfBq+fXfPGuDv
                             O+x1iQCJ5GQWQ3iUT20YA/L/16QmRXnuNZVjIsIZ1ddi7NRehdPleRxq5cbYOPR6
                             wVzoPIE1ARtoXmCREEmlLlEgr6tQLTEKy1uF7GvGU81neJX1l4yW9/+KKL+embph
                             4JGxWwHaReaVuN9hY0tpcoMdDk3mXamyplrYvGb9DMujtjNJlS78kB3sC5vvXb96
                             c+JKye8QH1inbIm4R7+bONJMBuLK7B8V2C9qSqUE+kJ2CRJeqvAgBBa9C0aOsCwp
                             uFeYVm2wtWTRqY5MoPq3imgZj5Vdi6942WAq2H1SFyMIq0RzWwgqpQA7zywIRP9H
                             zfyBAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFGYebL6kTZl9
                             alFHS7lNrqV5vRBVMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQDD+LnvVNsFWtfO5ODDWjZKQ+Kj1bSdveiJiAIgaq46
                             x6jybt/Ku1tYnOgWpXY5kYZdBQPLU0ho1SSwxFT/iIdqmBR6IvCSlLtvqXlVNKg+
                             w+GtMGuLESxgYjTmY9CzdUYFix9BN2YEmZpyv7l/zZ1dVohr4DLIy1RwQcITeiT0
                             oBxzQU4D0LKLixgjcjn1lCamgeADab0Ib3VwJtCNbG2vhGy7rIDMOf7uJoBjcq5+
                             eS45PIo6DwmjycnPC0o4wQpc9kyipaiTv6RH443OtCBP8hNS1nuHZW5/XjmWVo1q
                             QQlABLVuyM9DtkmPVU9s2+jsmOJ4bn9WFyhvhU/TsIuQ
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 23
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 23], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 24
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 7. 1. 2024 8:56:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABif8EBml8R08gAAAAAAGDANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yNDAxMDcw
                             ODQ2MzhaFw0yNDAxMjEwODQ2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDDFbZNQhE58edGFdvd
                             YSed62A4msPagPS8Hp7dsuogYRDInTFxhsBR5BLY/9dO+Yr254NIfo3QuAkpPfS4
                             tNr4ZQCyFjfLJiOj5yRhdYOeKfRGC+0kYFoVPxQuqF9898Ea31oGNBE7X+AIGQJo
                             TqlPCztUJi+Cq21TasJt5913xMFuiAckfg+d3oM6yfikvQc+njnd56tmUmvrLUZS
                             +eQJTiP/JyRglHfsczl+k0Imj5OGWHvjo8pgP2GTjGg5zqocf6aYv4ZRIcFRKqez
                             50We51Bnakbax/8CEvnzlRQWuiPg63ol6UW+KkfakEEJ80v+BtZJCbn7d5HbK19O
                             iO0hAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQUzhnmAr588h6Feyel910Jmxf0M54wGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQCfXvSIZmrzSfUSG7+8J0HkvPsGlygGjW/4K0k0NG5+
                             p+aeLU527UMg76eAAiTXODCaJZ0YtKfxrJU4fg00oT6tIJk+0aXYbgXqEcP8iC/r
                             vk2Pti+PhVATS8kyaCshfnJbCdXt14gbqoXaqGNxGuHeH/msS77PVGTjdK4GiQNX
                             BiMYyqQXmMKN7MXhb2ZyNqPhhoTGOuVT/aY3975Zk7wnZRBxZfIrgaIwTdskxEKo
                             cDgoB8CC9Oa/W4LdmRBBBRrX/Y36dSzoWWPS4Xay8Jj4RNdjukvkROzRa7oElczX
                             aylc5WkAimGU34wYHPMORESzw/hrTNfaQqJr5lO60inU
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 24
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 24], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 25
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 7. 1. 2024 16:00:00
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABmOS5/qhCbb6QAAAAAAGTANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yNDAxMDcx
                             NTUwMDBaFw0yNDAxMjExNTUwMDBaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCoEa4Y2AKtsOKCfhKj
                             bJZ5pTY8OS7rQy3FQ9AswkQCCdAFT/sUMsKkw6YazUmtDUVv55gu7hQcN1bjbQfT
                             2Zu3WrYOKf0y3nApWWj80r2FoYD6u+w1OU0CvCpEkamwq6a9d1sMgjZ3McEAliLU
                             3x4pf3/8SeMVhhKXyvElU9MeDhlYRa1xb6nYWHi4NFn+NYTAbmy91Ollwaq3Xa/5
                             8VLIHfF7hZs0YRwgaecPGSzE6IlbAdJi9Rl0O8zXGwowtSti6zVq6vPIUHdIIFOW
                             FmKpTKbZG5iog5vuonhcMl5Jw7/4Rnyr/ZlEW/up2tDVrcpjsuOgDfElC5PttA9+
                             YHZFAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFItD3p5kghc+
                             8717hqNCplSl9e0RMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQCd34+7u5ru0WyTTaNWd8LeDpSolaJUfkGHEkq3gbvo
                             NyMZTsUNz4B9CcwUgrhI4c1fw/gtXm8OsUo23t2n8jv50V+RCqkqYNvdMBtUSeGC
                             kKsK7knC6oPwIMVE/dAKmA4lEYKvOMM/47hPnQUpypCckQRCT0LmHTe4W0zM6bWA
                             g+jjD/t0Qfeh6vgyVR3ibcWAPSVzrEsYDwHZ5Jv2u3B3bMnPFdlgmcOgcS1uLQOm
                             FaTO5gSDmVBamIMiCTlC641oSrM9km0iL1jJ4gX3neH+bso9KL+fvikoOq17GHtu
                             J4103VkhLSrngoZmweDExSKiyk1RxrzjPWfcfd04Jbm5
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 25
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 25], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 26
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 19. 1. 2024 8:46:38
Request.CommonName         : 
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABpDpsu5OlBThQAAAAAAGjANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yNDAxMTkw
                             ODM2MzhaFw0yNDAyMDIwODM2MzhaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDoz1hwEZ/sJXkdswZO
                             gYtShCeoiY1SdYUV/CVRVa06oruk1coUWj9udTc9JuM1YYReGY/ukKGt4F5hupew
                             sgZsjKLJFwuYHsVqoCgimSIi4omg/tvHAkA02ho2rLb3UUvtDGYQLr56BqNOEp1z
                             4aJKM8mUETnVJUXiCq02eDv3WJ5k163hpQYsOn6XzJt2lTIFs44EjiJw0xUZ+NIa
                             5jj1nyUD7+tvSRT1cWQFPx9i4wY3kCJrVEfye3i8qngOptnF7edQlFQWU/2mElFK
                             10FTi50lwS/0B0IZY0cDra5YNXYwTqLlI+muB4Z/U1BjIZHyd1iVH52kHAeRCzoo
                             Yq+RAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADAfBgNVHSMEGDAWgBRVsBmYJz6H3NwZurkrfStqqnKR
                             BTAdBgNVHQ4EFgQU9LEjE2UcmaY0mYiyOk6C1cUNtqgwGwYDVR0RBBQwEoIQdG9j
                             c3AucGtpdC5sb2NhbDBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGgLwQt
                             Uy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0MA0G
                             CSqGSIb3DQEBCwUAA4IBAQDEZcZdcdTNb60SKL3Wanaaq/2y3aIpTrvG9EFpCMZe
                             9T3PrI3I7ecWqv+HWc4Armr0G9L1B/Zeg4tZw2WKRsv4cKtfhrgA+Rb2EIJCId8k
                             U/ZMYGW18zOle3YEAfz6SCxiWZmMgaimbcue4o8Lv3olpWWW74yRIv0Dv3D5/m/a
                             1GXCyIg1hiH7osqeXlwkc9nWowpzucum5Pkj1hyfPL3PUQp6ljBXbWXbmvmiIwHr
                             szFdyP6Fiei6I6aD3olibZ48tCyJssSoV5xNMF0ewTdOcX2P28zrufQtnlWJmzuA
                             Opz9hy7CbKuud8nxMh00fWyCCdyHIZmWsL2FYAtrpmH1
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 26
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 26], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 27
Request.StatusCode         : 0
Request.DispositionMessage : Issued
Request.RequesterName      : PKIT\\TOCSP$
Request.SubmittedWhen      : 19. 1. 2024 16:00:01
Request.CommonName         : tocsp.pkit.local
CertificateTemplate        : 1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124
RawCertificate             : MIIEbTCCA1WgAwIBAgITYAAAABt+o++YePytewAAAAAAGzANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yNDAxMTkx
                             NTUwMDFaFw0yNDAyMDIxNTUwMDFaMBsxGTAXBgNVBAMTEHRvY3NwLnBraXQubG9j
                             YWwwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDBeZT3eQ8EnE3nzrUN
                             +XcBIERV27T/GKK5qwEMfxqxnG70oxZwKQu4Rlb5Yt/E91BmmV3I+ojLedEuS9bB
                             V0FoeDlAsHLx/SOjuF03bk0Wb+0QIfaYyG/1B90mwq3b40fiUZhkl3zswqh46f4B
                             EAj9H6YlLwxuaa7gL0Qw/Wf03FdHZ5oE/96zy3qRXdWSj9bm1hEnG8vz7rbVZd2e
                             vRhhU6A+kxfVLwLlXtIOY4QEjrLLLZjlr7y/lSWHDMxkM2QeMoi7fuqbdynrgWuY
                             nCr8p5056OfLeFmH3OPb7ZMtpPWLvrbsxqnMlCBrBE/f7kvuWbpMs3juksTBrtjW
                             hwzNAgMBAAGjggFBMIIBPTA7BgkrBgEEAYI3FQcELjAsBiQrBgEEAYI3FQj/+l+C
                             4uoch82bJ4erpkGDkmI0gb7DKYOguVQCAWQCAQIwEwYDVR0lBAwwCgYIKwYBBQUH
                             AwkwDgYDVR0PAQH/BAQDAgeAMBsGCSsGAQQBgjcVCgQOMAwwCgYIKwYBBQUHAwkw
                             DwYJKwYBBQUHMAEFBAIFADBOBgkrBgEEAYI3GQIEQTA/oD0GCisGAQQBgjcZAgGg
                             LwQtUy0xLTUtMjEtMTA0MjA5NTAzNi0zNjgyMzA4MzUtMzg0MTI1MzA4OS0xMTA0
                             MBsGA1UdEQQUMBKCEHRvY3NwLnBraXQubG9jYWwwHQYDVR0OBBYEFAq9HoHAHaL5
                             ciKRwfE3HfkVS4pfMB8GA1UdIwQYMBaAFFWwGZgnPofc3Bm6uSt9K2qqcpEFMA0G
                             CSqGSIb3DQEBCwUAA4IBAQB/u0QVgwioLx5SNbL98sG560+mmAd/WghKPQXbj2AG
                             X+DAouAlW/Oj40NnPal7Jk7qO9bXtPDwEkgM1fLHOolHK3uTa3dg6pVU5CFqRPQt
                             M0CPGLskcvq0VaiplWWpTu0excN1k6E76aYhUym8/L8AXTtAZ3pWF2ONtqkmjPpT
                             PU5M2AYSrY3ApXDlcJHapoNLMuTR31fHHmvnTe+6vPRIECi1tZbEd8KniSK4/w81
                             T4oT8aMUXtbCPna+HBUTpf9RALxBeUxAZrzpw46VeslFDJHSmZDLYsXpkuwzYMwR
                             ONHLrALdzEXvacikRU77fbI+a7FsjosUIWUi4Oi+jSbs
                             
CertificateTemplateOid     : PKIT OCSP Response Signing (1.3.6.1.4.1.311.21.8.2096479.5813532.15945127.15389505.51554.52.3121577.6823124)
RowId                      : 27
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 27], [Request.StatusCode, 0], [Request.DispositionMessage, Issued], [Request.RequesterName, PKIT\\TOCSP$]...}

RequestID                  : 4
Request.StatusCode         : 0
Request.DispositionMessage : Revoked by PKIT\\mrublik00
Request.RequesterName      : PKIT\\TICA$
Request.SubmittedWhen      : 3. 10. 2023 10:17:20
Request.CommonName         : TEST Slovak Telekom Issuing CA 02 Class B-Xchg
CertificateTemplate        : CAExchange
RawCertificate             : MIIFzjCCBLagAwIBAgITYAAAAAQJvVYf2TDNGAAAAAAABDANBgkqhkiG9w0BAQsF
                             ADCBgTELMAkGA1UEBhMCU0sxEzARBgNVBAcTCkJyYXRpc2xhdmExHDAaBgNVBAoT
                             E1Nsb3ZhayBUZWxla29tIGEucy4xCzAJBgNVBAsTAklUMTIwMAYDVQQDEylURVNU
                             IFNsb3ZhayBUZWxla29tIElzc3VpbmcgQ0EgMDIgQ2xhc3MgQjAeFw0yMzEwMDMx
                             MDA3MjBaFw0yMzEwMTAxMDE3MjBaMIGGMQswCQYDVQQGEwJTSzETMBEGA1UEBxMK
                             QnJhdGlzbGF2YTEcMBoGA1UEChMTU2xvdmFrIFRlbGVrb20gYS5zLjELMAkGA1UE
                             CxMCSVQxNzA1BgNVBAMTLlRFU1QgU2xvdmFrIFRlbGVrb20gSXNzdWluZyBDQSAw
                             MiBDbGFzcyBCLVhjaGcwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDK
                             lYBWiScuPLTSpGWwOF01WilxqSM1DttxqZ2plmmXQ2zJBRISr9zYg9JoNMxV1bxI
                             Z+8BqWBSBoo30wcCvOgPfnyP8MOfuIAUBUGXhseufcNeIAnjhgCKbynvF1wt5qx3
                             +kLCZLiqqhsh//XHeJ6xES/RbiM9uKpfkEe0IwiapS1WwCc+jyhOAXUM4+vfIU2H
                             Cij1v5IZC36rwr1jjCSMLeIu5GoyKHgf416MPTNBJxHjaIHLVtqOY7qumCRUpzZn
                             w3HJ9a13RXGuGoC5YVl47JXo4rrDWuhX6SFpQiX9GmuNjxxTwe3FFVTiP+TcHSmM
                             +4PPQpRcmm+PMRGfR8LBAgMBAAGjggI2MIICMjAdBgNVHQ4EFgQU1lPT+OaGiqq6
                             q9ABImVq3E73zycwHwYDVR0jBBgwFoAUVbAZmCc+h9zcGbq5K30raqpykQUwawYD
                             VR0fBGQwYjBgoF6gXIZaaHR0cDovL2NkcC10ZXN0LnN0LnNrL0NlcnREYXRhL1RF
                             U1QlMjBTbG92YWslMjBUZWxla29tJTIwSXNzdWluZyUyMENBJTIwMDIlMjBDbGFz
                             cyUyMEIuY3JsMIGgBggrBgEFBQcBAQSBkzCBkDAmBggrBgEFBQcwAYYaaHR0cDov
                             L2NkcC10ZXN0LnN0LnNrL29jc3AwZgYIKwYBBQUHMAKGWmh0dHA6Ly9jZHAtdGVz
                             dC5zdC5zay9DZXJ0RGF0YS9URVNUJTIwU2xvdmFrJTIwVGVsZWtvbSUyMElzc3Vp
                             bmclMjBDQSUyMDAyJTIwQ2xhc3MlMjBCLmNydDAjBgkrBgEEAYI3FAIEFh4UAEMA
                             QQBFAHgAYwBoAGEAbgBnAGUwQAYDVR0gBDkwNzA1BgwrBgEEAYKULQEBAgEwJTAj
                             BggrBgEFBQcCARYXaHR0cDovL3BraS5zdC5zay9DbGFzc0IwNQYJKwYBBAGCNxUH
                             BCgwJgYeKwYBBAGCNxUI//pfguLqHIfNmyeHq6ZBg5JiNAEaAgFqAgEAMBQGA1Ud
                             JQQNMAsGCSsGAQQBgjcVBTAOBgNVHQ8BAf8EBAMCBSAwHAYJKwYBBAGCNxUKBA8w
                             DTALBgkrBgEEAYI3FQUwDQYJKoZIhvcNAQELBQADggEBAIscVaMnDe+RhtN2AG9O
                             6LE05vgagQPaMFDBLEYrVkgArerIzqO2VQqHduAu/x9KdT/bgw/GhtO6gqeBL4ty
                             QoQPlq5FrKrvvsdmMTzVeV3/tjtWMm0IGrjTMml7NAcN/32DBdYbsRCEtkxM7dDw
                             M9XpmMTuJaJogoyrEP8vu0pypDMELCbTeJFg7vcxmKqSoMQ+fL/ux3VxIDqu85oj
                             t/f9swMYkWtp84jq9c/oJigceH7pZnaHmgz0Ati4bN+IHAilpmJ+1bhJhrOrPKZU
                             eQfNpHqyXxL3Y2LBCgiKvCVu+OMZ+G90Nq3czDOJ2/2g88aFvtX+ys4AJrWAm6uw
                             Slw=
                             
CertificateTemplateOid     : CAExchange
RowId                      : 4
ConfigString               : tica.pkit.local\\TEST Slovak Telekom Issuing CA 02 Class B
Table                      : Request
Properties                 : {[RequestID, 4], [Request.StatusCode, 0], [Request.DispositionMessage, Revoked by PKIT\\mrublik00], [Request.RequesterName, PKIT\\TICA$]...}


        """
        protocol_output = bytes(data, 'utf-8'), bytes(data, 'utf-8'), 0
        result = winrm.Response(protocol_output)
        templates = DumpParser.parse_certificates(result)
        self.assertEqual(len(templates), 25)
        # self.assertEqual(templates[0].template, "WebServer")
