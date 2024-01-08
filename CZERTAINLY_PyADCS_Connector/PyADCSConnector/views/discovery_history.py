import json
import logging
import threading
from threading import Thread

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from CZERTAINLY_PyADCS_Connector.settings import ADCS_SEARCH_PAGE_SIZE
from PyADCSConnector.models.discovery_certificate import DiscoveryCertificate
from PyADCSConnector.models.discovery_history import DiscoveryHistory
from PyADCSConnector.remoting.winrm.scripts import get_cas_script, dump_certificates_script
from PyADCSConnector.remoting.winrm_remoting import create_session_from_authority_instance
from PyADCSConnector.services.attributes.discovery_attributes import *
from PyADCSConnector.services.attributes.metadata_attributes import get_ca_name_metadata_attribute, \
    get_template_name_metadata_attribute
from PyADCSConnector.utils import attribute_definition_utils
from PyADCSConnector.utils.ca_select_method import CaSelectMethod
from PyADCSConnector.utils.discovery_status import DiscoveryStatus
from PyADCSConnector.utils.dump_parser import DumpParser, AuthorityData, TemplateData
from PyADCSConnector.views.authority_instance import AuthorityInstanceAttributeObject

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
def start_discovery(request, *args, **kwargs):
    form = json.loads(request.body)
    validate_discovery_kind(form["kind"])

    if DiscoveryHistory.objects.filter(name=form["name"]).exists():
        return JsonResponse({"message": "Discovery with name %s already exists" % form["name"]}, status=400)

    discovery_history = create_discovery_history(form)

    # create a new thread and run discovery
    # TODO: make running the discovery asynchronous
    # run_discovery(form, discovery_history)

    Thread(target=run_discovery, args=(form, discovery_history.uuid), daemon=True).start()

    discovery_history_request = dict()
    discovery_history_request["name"] = form["name"]
    discovery_history_request["pageNumber"] = 0
    discovery_history_request["itemsPerPage"] = 10

    discovery_history_data_response = get_discovery_history_data(discovery_history_request, discovery_history)

    return JsonResponse(discovery_history_data_response, safe=False, content_type="application/json")


@require_http_methods(["POST", "DELETE"])
@transaction.atomic
def discovery_operations(request, uuid, *args, **kwargs):
    if request.method == "DELETE":
        try:
            discovery_history = DiscoveryHistory.objects.get(uuid=uuid)
            discovery_certificates = DiscoveryCertificate.objects.filter(discovery_id=discovery_history.id)
            discovery_certificates.delete()
            discovery_history.delete()
            # return 204 no content
            return JsonResponse({}, status=204)
        except DiscoveryHistory.DoesNotExist:
            return JsonResponse({"message": "Requested Discovery History with UUID %s not found" % uuid}, status=404)
    else:
        try:
            discovery_history = DiscoveryHistory.objects.get(uuid=uuid)
            discovery_history_request = json.loads(request.body)
            discovery_history_data_response = get_discovery_history_data(discovery_history_request, discovery_history)
            return JsonResponse(discovery_history_data_response, safe=False, content_type="application/json")
        except DiscoveryHistory.DoesNotExist:
            return JsonResponse({"message": "Requested Discovery History with UUID %s not found" % uuid}, status=404)


@transaction.atomic
def create_discovery_history(form):
    discovery_history: DiscoveryHistory = DiscoveryHistory()
    discovery_history.name = form["name"]
    discovery_history.status = DiscoveryStatus.IN_PROGRESS.value

    discovery_history.save()

    return discovery_history


# Run certificate discovery asynchronously
def run_discovery(form, discovery_history_uuid):
    logger.debug("Starting discovery for %s in a new thread %s" % (form["name"], threading.get_ident()))
    discovery_history = DiscoveryHistory.objects.get(uuid=discovery_history_uuid)
    try:
        discover_certificates(form, discovery_history)
    except Exception as e:
        discovery_history.status = DiscoveryStatus.FAILED.value
        discovery_history.save()
        raise e


@transaction.atomic
def discover_certificates(form, discovery_history):
    logger.info("Starting discovery for %s" % form["name"])

    select_ca_method = attribute_definition_utils.get_attribute_value(
        DISCOVERY_SELECT_CA_METHOD_ATTRIBUTE_NAME, form["attributes"])
    authority_instance = AuthorityInstanceAttributeObject.from_dict(
        attribute_definition_utils.get_attribute_value(DISCOVERY_AUTHORITY_INSTANCE_ATTRIBUTE_NAME, form["attributes"]))

    authority = AuthorityInstance.objects.get(uuid=authority_instance.uuid)

    if select_ca_method == CaSelectMethod.SEARCH.method:
        cas = AuthorityData.from_dicts(
            attribute_definition_utils.get_attribute_value_list(DISCOVERY_CA_NAME_ATTRIBUTE_NAME, form["attributes"]))
    elif select_ca_method == CaSelectMethod.CONFIGSTRING.method:
        config_string = attribute_definition_utils.get_attribute_value(
            DISCOVERY_CONFIGSTRING_ATTRIBUTE_NAME, form["attributes"])
        if not config_string:
            raise Exception("ConfigString is required with selected CA Method: " + select_ca_method)
        ca_name = config_string.split("\\")[1]
        computer_name = config_string.split("\\")[0]
        if not ca_name or not computer_name:
            raise Exception("Wrong format of ConfigString: " + config_string)
        cas = [AuthorityData(
            config_string.split("\\")[1], config_string.split("\\")[1], config_string.split("\\")[0],
            config_string, "", None, None)]
    else:
        raise Exception("Unknown CA Select Method: " + select_ca_method)

    templates = TemplateData.from_dicts(
        attribute_definition_utils.get_attribute_value_list(DISCOVERY_TEMPLATE_NAME_ATTRIBUTE_NAME, form["attributes"]))
    issued_after = attribute_definition_utils.get_attribute_value(DISCOVERY_ISSUED_AFTER_ATTRIBUTE_NAME, form["attributes"])

    logger.debug("Authority instance: %s, CA names: %s, Template names: %s" %
                 (authority_instance, cas, templates))

    session = create_session_from_authority_instance(authority)
    session.connect()

    # if ca_names is empty, then get all CAs
    # TODO: This operation may timeout if there are too many CAs, especially when their are not accessible,
    #  it should be handled
    if not cas:
        result = session.run_ps(get_cas_script())
        cas = DumpParser.parse_authority_data(result)

    total_certificates = []
    for ca in cas:
        if not templates:
            page = 1
            result = session.run_ps(dump_certificates_script(ca, None, issued_after, 1, ADCS_SEARCH_PAGE_SIZE))
            certificates = DumpParser.parse_certificates(result)
            total_certificates.extend(certificates)
            while len(certificates) == ADCS_SEARCH_PAGE_SIZE:
                page += 1
                result = session.run_ps(dump_certificates_script(ca, None, issued_after, page, ADCS_SEARCH_PAGE_SIZE))
                certificates = DumpParser.parse_certificates(result)
                total_certificates.extend(certificates)
        else:
            for template in templates:
                page = 1
                result = session.run_ps(dump_certificates_script(ca, template, issued_after, page, ADCS_SEARCH_PAGE_SIZE))
                certificates = DumpParser.parse_certificates(result)
                total_certificates.extend(certificates)
                while len(certificates) == ADCS_SEARCH_PAGE_SIZE:
                    page += 1
                    result = session.run_ps(dump_certificates_script(ca, template, issued_after, page, ADCS_SEARCH_PAGE_SIZE))
                    certificates = DumpParser.parse_certificates(result)
                    total_certificates.extend(certificates)

    session.disconnect()

    for certificate in total_certificates:
        discovery_certificate = DiscoveryCertificate()
        discovery_certificate.discovery_id = discovery_history.id
        discovery_certificate.base64content = certificate.certificate
        discovery_certificate.meta = get_certificate_meta(cas, certificate.template)
        discovery_certificate.save()

    logger.info("Discovery %s has total %d certificates" % (form["name"], len(total_certificates)))

    discovery_history.status = DiscoveryStatus.COMPLETED.value
    discovery_history.save()

    logger.info("Discovery %s completed" % form["name"])


def get_discovery_history_data(discovery_history_request, discovery_history):
    discovery_response = dict()
    discovery_response["uuid"] = discovery_history.uuid
    discovery_response["name"] = discovery_history.name
    discovery_response["status"] = discovery_history.status
    discovery_response["meta"] = discovery_history.meta
    total_certificates = DiscoveryCertificate.objects.filter(discovery_id=discovery_history.id).count()
    discovery_response["totalCertificatesDiscovered"] = total_certificates
    if discovery_history.status == DiscoveryStatus.IN_PROGRESS:
        discovery_response["certificateData"] = []
        discovery_response["totalCertificatesDiscovered"] = 0
    else:
        page_number = 0 if discovery_history_request["pageNumber"] <= 0 else discovery_history_request["pageNumber"] - 1
        items_per_page = discovery_history_request["itemsPerPage"]

        # select from DiscoveryCertificate where discovery_id = discovery_history.id limit items_per_page offset
        # page_number * items_per_page
        # discovery_certificates = DiscoveryCertificate.objects.filter(
        #     discovery_id=discovery_history.id)[page_number * items_per_page:items_per_page]
        discovery_certificates = DiscoveryCertificate.objects.filter(
            discovery_id=discovery_history.id
        )[page_number * items_per_page:(page_number + 1) * items_per_page]

        discovery_response["certificateData"] = [
            {"uuid": str(val.uuid), "base64Content": val.base64content, "meta": val.meta}
            for val in discovery_certificates
        ]
    return discovery_response


def get_certificate_meta(cas, template_name):
    meta_list = [get_ca_name_metadata_attribute(cas[0].name), get_template_name_metadata_attribute(template_name)]

    return meta_list
