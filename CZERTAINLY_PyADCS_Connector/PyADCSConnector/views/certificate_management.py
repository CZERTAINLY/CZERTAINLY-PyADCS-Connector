import base64
import json
import logging

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from PyADCSConnector.remoting.winrm.scripts import submit_certificate_request_script, identify_certificate_script, \
    get_revoke_script
from PyADCSConnector.remoting.winrm_remoting import create_session_from_authority_instance_uuid
from PyADCSConnector.services.attributes.raprofile_attributes import *
from PyADCSConnector.utils import attribute_definition_utils
from PyADCSConnector.utils.ca_select_method import CaSelectMethod
from PyADCSConnector.utils.dump_parser import DumpParser, AuthorityData, TemplateData

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def issue_certificate(request, uuid, *args, **kwargs):
    return issue(request, uuid)


@require_http_methods(["POST"])
def renew_certificate(request, uuid, *args, **kwargs):
    return renew(request, uuid)


@require_http_methods(["POST"])
def revoke_certificate(request, uuid, *args, **kwargs):
    return revoke(request, uuid)


@require_http_methods(["POST"])
def identify_certificate(request, uuid, *args, **kwargs):
    return identify(request, uuid)


def issue(request, uuid):
    form = json.loads(request.body)

    ca = get_ca_from_attributes(form)

    template = TemplateData.from_dict(
        attribute_definition_utils.get_attribute_value(
            RAPROFILE_TEMPLATE_NAME_ATTRIBUTE_NAME, form["raProfileAttributes"]))

    return issue_new_certificate(uuid, form["pkcs10"], ca, template)


def renew(request, uuid):
    form = json.loads(request.body)

    ca = get_ca_from_attributes(form)

    template = TemplateData.from_dict(
        attribute_definition_utils.get_attribute_value(
            RAPROFILE_TEMPLATE_NAME_ATTRIBUTE_NAME, form["raProfileAttributes"]))

    serial_number = get_certificate_serial_number(form["certificate"])

    logger.debug("Renew certificate with serial number %s" % serial_number)

    return issue_new_certificate(uuid, form["pkcs10"], ca, template)


def revoke(request, uuid):
    form = json.loads(request.body)

    ca = get_ca_from_attributes(form)

    reason = form["reason"]
    serial_number = get_certificate_serial_number(form["certificate"])

    session = create_session_from_authority_instance_uuid(uuid)
    session.connect()
    session.run_ps(get_revoke_script(ca, serial_number, reason))
    session.disconnect()

    return JsonResponse({}, safe=False, content_type="application/json")


def identify(request, uuid):
    form = json.loads(request.body)

    ca = get_ca_from_attributes(form)

    template = TemplateData.from_dict(
        attribute_definition_utils.get_attribute_value(
            RAPROFILE_TEMPLATE_NAME_ATTRIBUTE_NAME, form["raProfileAttributes"]))
    certificate = form["certificate"]

    # Convert certificate to x509 using cryptography module, it should be in base64 format
    x509_cert = x509.load_der_x509_certificate(base64.b64decode(certificate), default_backend())
    serial_number = '{0:x}'.format(x509_cert.serial_number)

    session = create_session_from_authority_instance_uuid(uuid)
    session.connect()
    logger.debug("Identify certificate with serial number %s" % serial_number)
    result = session.run_ps(identify_certificate_script(serial_number, ca))
    session.disconnect()

    parsed = DumpParser.parse_identified_certificates(result)
    if not parsed:
        return JsonResponse({"message": "Certificate not found"}, status=404)
    elif len(parsed) > 1:  # this should not happen, CA should not issue 2 certificates with the same SN
        return JsonResponse({"message": "More than one certificate found"}, status=422)
    else:  # we have one certificate issued by the CA
        if parsed[0].certificate_template == template.oid or parsed[0].certificate_template == template.name:
            response = dict()
            response["meta"] = []
            return JsonResponse(response, safe=False, content_type="application/json")
        else:
            return JsonResponse({"message": "Certificate found but template does not match according to RA Profile "
                                            "attributes"}, status=422)


def issue_new_certificate(uuid, certificate_request, ca: AuthorityData, template: TemplateData):
    session = create_session_from_authority_instance_uuid(uuid)
    session.connect()
    result = session.run_ps(submit_certificate_request_script(certificate_request, ca, template))
    session.disconnect()

    # Remove new lines and empty lines to form one Base64 string
    certificate = get_certificate_data(result)
    # If certificate is empty
    if not certificate:
        return JsonResponse({"message": "Output of the certificate is empty"}, status=500)

    response = dict()
    response["certificateData"] = certificate

    return JsonResponse(response, safe=False, content_type="application/json")


def get_certificate_data(result):
    input_string = result.std_out.decode('utf-8')
    return ''.join(input_string.splitlines())


def get_certificate_serial_number(certificate):
    """
    Get serial number from certificate in base64 format
    :param certificate: certificate in base64 format
    :return: serial number in hex format
    """
    x509_cert = x509.load_der_x509_certificate(base64.b64decode(certificate), default_backend())
    return '{0:x}'.format(x509_cert.serial_number)


def get_ca_from_attributes(form):
    select_ca_method = attribute_definition_utils.get_attribute_value(
        RAPROFILE_SELECT_CA_METHOD_ATTRIBUTE_NAME, form["raProfileAttributes"])

    if select_ca_method == CaSelectMethod.SEARCH.method:
        ca = AuthorityData.from_dict(
            attribute_definition_utils.get_attribute_value(
                RAPROFILE_CA_NAME_ATTRIBUTE_NAME, form["raProfileAttributes"]))
    elif select_ca_method == CaSelectMethod.CONFIGSTRING.method:
        config_string = attribute_definition_utils.get_attribute_value(
            RAPROFILE_CONFIGSTRING_ATTRIBUTE_NAME, form["raProfileAttributes"])
        if not config_string:
            raise Exception("ConfigString is required with selected CA Method: " + select_ca_method)
        ca_name = config_string.split("\\")[1]
        computer_name = config_string.split("\\")[0]
        if not ca_name or not computer_name:
            raise Exception("Wrong format of ConfigString: " + config_string)
        ca = AuthorityData(
            config_string.split("\\")[1], config_string.split("\\")[1], config_string.split("\\")[0],
            config_string, "", None, None)
    else:
        raise Exception("Unknown CA Select Method: " + select_ca_method)

    return ca
