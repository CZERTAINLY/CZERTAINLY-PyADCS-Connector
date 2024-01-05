"""
Script to perform attribute related operations like getting attributes,
validate attributes
"""
from typing import List

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.remoting.winrm.scripts import get_templates_script
from PyADCSConnector.remoting.winrm_remoting import create_session_from_authority_instance
from PyADCSConnector.utils.ca_select_method import CaSelectMethod
from PyADCSConnector.utils.dump_parser import DumpParser, AuthorityData, TemplateData
from PyADCSConnector.views.constants import *


@require_http_methods(["GET"])
def get_attributes(request, kind, *args, **kwargs):
    try:
        return JsonResponse(get_attributes_list(kind), safe=False, content_type="application/json")
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@require_http_methods(["GET"])
def get_discovery_attributes(request, kind, *args, **kwargs):
    try:
        return JsonResponse(get_discovery_attributes_list(kind), safe=False, content_type="application/json")
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@require_http_methods(["GET"])
def get_raprofile_attributes(request, uuid, *args, **kwargs):
    try:
        return JsonResponse(get_raprofile_attributes_list(uuid), safe=False, content_type="application/json")
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@require_http_methods(["GET"])
def get_issue_attributes(request, uuid, *args, **kwargs):
    try:
        attribute_list = []
        return JsonResponse(attribute_list, safe=False, content_type="application/json")
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@require_http_methods(["GET"])
def get_revoke_attributes(request, uuid, *args, **kwargs):
    try:
        attribute_list = []
        return JsonResponse(attribute_list, safe=False, content_type="application/json")
    except ValueError as e:
        return JsonResponse({"message": str(e)}, status=400)


@require_http_methods(["POST"])
def validate_attributes(request, kind, *args, **kwargs):
    # TODO: Implement validation of attributes
    return HttpResponse(content_type="application/json", status=200)


@require_http_methods(["POST"])
def validate_discovery_attributes(request, kind, *args, **kwargs):
    # TODO: Implement validation of attributes
    return HttpResponse(content_type="application/json", status=200)


@require_http_methods(["POST"])
def validate_raprofile_attributes(request, uuid, *args, **kwargs):
    # TODO: Implement validation of attributes
    return HttpResponse(content_type="application/json", status=200)


@require_http_methods(["POST"])
def validate_issue_attributes(request, uuid, *args, **kwargs):
    # TODO: Implement validation of attributes
    return HttpResponse(content_type="application/json", status=200)


@require_http_methods(["POST"])
def validate_revoke_attributes(request, uuid, *args, **kwargs):
    # TODO: Implement validation of attributes
    return HttpResponse(content_type="application/json", status=200)


def validate_kind(kind):
    if kind != "PyADCS-WinRM":
        raise ValueError("Unrecognized kind: %s" % kind)


def get_attributes_list(kind):
    attribute_list = []

    if kind != "PyADCS-WinRM":
        raise ValueError("Unrecognized kind: %s" % kind)

    attribute_list.append(get_adcs_info_attribute())
    attribute_list.append(get_credential_type_attribute())
    attribute_list.append(get_credential_attribute())
    attribute_list.append(get_server_attribute())
    attribute_list.append(get_use_https_attribute())
    attribute_list.append(get_winrm_port_attribute())
    attribute_list.append(get_winrm_transport_attribute())

    return attribute_list


def get_discovery_attributes_list(kind):
    attribute_list = []

    if kind != "PyADCS-WinRM":
        raise ValueError("Unrecognized kind: %s" % kind)

    attribute_list.append(get_discovery_info_attribute())
    attribute_list.append(get_authority_instances_attribute(kind))
    attribute_list.append(get_select_ca_method_attribute())
    attribute_list.append(get_ca_select_group_attribute())
    attribute_list.append(get_template_name_attribute())
    attribute_list.append(get_issued_after_attribute())

    return attribute_list


def get_raprofile_attributes_list(uuid):
    authority_instance = AuthorityInstance.objects.get(uuid=uuid)

    session = create_session_from_authority_instance(authority_instance)
    session.connect()
    templates = session.run_ps(get_templates_script())
    session.disconnect()

    templates = DumpParser.parse_template_data(templates)

    attribute_list = [get_select_ca_method_attribute(),
                      get_authority_uuid_attribute(uuid),
                      get_ca_select_group_ra_profile_attribute(),
                      get_template_name_ra_profile_attribute(templates)]

    return attribute_list


def get_winrm_transport_configuration_attributes_list(kind, winrm_transport):
    if kind != "PyADCS-WinRM":
        raise ValueError("Unrecognized kind: %s" % kind)

    if winrm_transport != "credssp":
        raise ValueError("Unrecognized protocol: %s" % winrm_transport)

    # attribute_list = []

    match winrm_transport:
        case "credssp":
            return


def get_all_attributes_list(kind, winrm_transport):
    if kind != "PyADCS-WinRM":
        raise ValueError("Unrecognized kind: %s" % kind)

    if winrm_transport != "credssp":
        raise ValueError("Unrecognized protocol: %s" % winrm_transport)

    attribute_list = [get_adcs_info_attribute(), get_credential_type_attribute(), get_credential_attribute(),
                      get_server_attribute(), get_use_https_attribute(), get_winrm_port_attribute(),
                      get_winrm_transport_attribute(), get_winrm_transport_config_attribute(kind)]
    return attribute_list


def get_adcs_info_attribute():
    adcs_info_attribute = dict()
    adcs_info_attribute[NAME_ATTRIBUTE_PROPERTY] = ADCS_INFO_ATTRIBUTE_NAME
    adcs_info_attribute[UUID_ATTRIBUTE_PROPERTY] = ADCS_INFO_ATTRIBUTE_UUID
    adcs_info_attribute[TYPE_ATTRIBUTE_PROPERTY] = "info"
    adcs_info_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "text"
    adcs_info_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = ADCS_INFO_ATTRIBUTE_DESCRIPTION
    adcs_info_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_info_attribute_properties(
        ADCS_INFO_ATTRIBUTE_LABEL,
        is_visible=True)
    markdown_string = """
### ADCS authority instance configuration using WinRM protocol

Choose the credential and server configuration to proceed.
    """
    adcs_info_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"data": markdown_string},
    ]
    return adcs_info_attribute


def get_credential_type_attribute():
    credential_type_attribute = dict()
    credential_type_attribute[NAME_ATTRIBUTE_PROPERTY] = CREDENTIAL_TYPE_ATTRIBUTE_NAME
    credential_type_attribute[UUID_ATTRIBUTE_PROPERTY] = CREDENTIAL_TYPE_ATTRIBUTE_UUID
    credential_type_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    credential_type_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    credential_type_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = CREDENTIAL_TYPE_ATTRIBUTE_DESCRIPTION
    credential_type_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        CREDENTIAL_TYPE_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    credential_type_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": "Basic", "data": "Basic"},
    ]
    return credential_type_attribute


def get_credential_attribute():
    credential_attribute = dict()
    credential_attribute[NAME_ATTRIBUTE_PROPERTY] = CREDENTIAL_ATTRIBUTE_NAME
    credential_attribute[UUID_ATTRIBUTE_PROPERTY] = CREDENTIAL_ATTRIBUTE_UUID
    credential_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    credential_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "credential"
    credential_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = CREDENTIAL_ATTRIBUTE_DESCRIPTION
    credential_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        CREDENTIAL_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    credential_attribute_callback = {
        "callbackContext": "core/getCredentials",
        "callbackMethod": "GET",
        "mappings": [
            {
                "from": "credential_type",
                "to": "credentialKind",
                "targets": [
                    "pathVariable"
                ]
            }
        ]
    }
    credential_attribute[PROPERTY_ATTRIBUTE_CALLBACK] = credential_attribute_callback
    return credential_attribute


def get_winrm_transport_attribute():
    winrm_transport_attribute = dict()
    winrm_transport_attribute[NAME_ATTRIBUTE_PROPERTY] = WINRM_TRANSPORT_ATTRIBUTE_NAME
    winrm_transport_attribute[UUID_ATTRIBUTE_PROPERTY] = WINRM_TRANSPORT_ATTRIBUTE_UUID
    winrm_transport_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    winrm_transport_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    winrm_transport_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = WINRM_TRANSPORT_ATTRIBUTE_DESCRIPTION
    winrm_transport_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        WINRM_TRANSPORT_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    winrm_transport_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": "CredSSP", "data": "credssp"},
    ]
    return winrm_transport_attribute


def get_winrm_transport_config_attribute(kind):
    winrm_transport_config_attribute = dict()
    winrm_transport_config_attribute[NAME_ATTRIBUTE_PROPERTY] = WINRM_TRANSPORT_CONFIG_ATTRIBUTE_NAME
    winrm_transport_config_attribute[UUID_ATTRIBUTE_PROPERTY] = WINRM_TRANSPORT_CONFIG_ATTRIBUTE_UUID
    winrm_transport_config_attribute[TYPE_ATTRIBUTE_PROPERTY] = "group"
    winrm_transport_config_attribute_callback = {
        "callbackContext": "/v1/authorityProvider/{kind}/{winrm_transport}",
        "callbackMethod": "GET",
        "mappings": [
            {
                "from": "winrm_transport.data",
                "to": "winrm_transport",
                "targets": [
                    "pathVariable"
                ]
            },
            {
                "to": "kind",
                "targets": [
                    "pathVariable"
                ],
                "value": kind
            }
        ]
    }
    winrm_transport_config_attribute[PROPERTY_ATTRIBUTE_CALLBACK] = winrm_transport_config_attribute_callback
    return winrm_transport_config_attribute


def get_server_attribute():
    server_attribute = dict()
    server_attribute[NAME_ATTRIBUTE_PROPERTY] = SERVER_ADDRESS_ATTRIBUTE_NAME
    server_attribute[UUID_ATTRIBUTE_PROPERTY] = SERVER_ADDRESS_ATTRIBUTE_UUID
    server_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    server_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    server_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = SERVER_ADDRESS_ATTRIBUTE_DESCRIPTION
    server_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        SERVER_ADDRESS_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=False,
        is_multi_select=False)
    server_attribute[CONSTRAINTS_ATTRIBUTE_PROPERTY] = dict()
    server_regexp_constraint = dict()
    server_regexp_constraint["type"] = "regExp"
    server_regexp_constraint["description"] = "Address of ADCS Server"
    server_regexp_constraint["errorMessage"] = "Enter Valid Address"
    server_regexp_constraint["data"] = ("^((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|"
                                           "[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])|(([a-zA-Z0-9]|[a-zA-Z0-9]"
                                           "[a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([A-Za-z0-9]|[A-Za-z0-9]"
                                           "[A-Za-z0-9\\-]*"
                                           "[A-Za-z0-9]))$")
    server_attribute[CONSTRAINTS_ATTRIBUTE_PROPERTY] = [server_regexp_constraint]
    return server_attribute


def get_use_https_attribute():
    use_https_attribute = dict()
    use_https_attribute[NAME_ATTRIBUTE_PROPERTY] = USE_HTTPS_ATTRIBUTE_NAME
    use_https_attribute[UUID_ATTRIBUTE_PROPERTY] = USE_HTTPS_ATTRIBUTE_UUID
    use_https_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    use_https_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "boolean"
    use_https_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = USE_HTTPS_ATTRIBUTE_DESCRIPTION
    use_https_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        USE_HTTPS_ATTRIBUTE_LABEL,
        is_required=False,
        is_read_only=False,
        is_visible=True,
        is_list=False,
        is_multi_select=False)
    use_https_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": "True", "data": "true"},
    ]
    return use_https_attribute


def get_winrm_port_attribute():
    winrm_port_attribute = dict()
    winrm_port_attribute[NAME_ATTRIBUTE_PROPERTY] = WINRM_PORT_ATTRIBUTE_NAME
    winrm_port_attribute[UUID_ATTRIBUTE_PROPERTY] = WINRM_PORT_ATTRIBUTE_UUID
    winrm_port_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    winrm_port_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "integer"
    winrm_port_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = WINRM_PORT_ATTRIBUTE_DESCRIPTION
    winrm_port_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        WINRM_PORT_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=False,
        is_multi_select=False)
    winrm_port_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": "5985", "data": "5985"},
    ]
    return winrm_port_attribute


def get_select_ca_method_attribute():
    select_ca_method_attribute = dict()
    select_ca_method_attribute[NAME_ATTRIBUTE_PROPERTY] = SELECT_CA_METHOD_ATTRIBUTE_NAME
    select_ca_method_attribute[UUID_ATTRIBUTE_PROPERTY] = SELECT_CA_METHOD_ATTRIBUTE_UUID
    select_ca_method_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    select_ca_method_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    select_ca_method_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = SELECT_CA_METHOD_ATTRIBUTE_DESCRIPTION
    select_ca_method_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        SELECT_CA_METHOD_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    select_ca_method_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": method.description, "data": method.method} for method in CaSelectMethod
    ]
    return select_ca_method_attribute


def get_config_string_attribute():
    computer_name_attribute = dict()
    computer_name_attribute[NAME_ATTRIBUTE_PROPERTY] = CONFIGSTRING_ATTRIBUTE_NAME
    computer_name_attribute[UUID_ATTRIBUTE_PROPERTY] = CONFIGSTRING_ATTRIBUTE_UUID
    computer_name_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    computer_name_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    computer_name_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = CONFIGSTRING_ATTRIBUTE_DESCRIPTION
    computer_name_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        CONFIGSTRING_ATTRIBUTE_LABEL,
        is_required=False,
        is_read_only=False,
        is_visible=True,
        is_list=False,
        is_multi_select=False)
    return computer_name_attribute


def get_ca_select_group_attribute():
    ca_select_group_attribute = dict()
    ca_select_group_attribute[NAME_ATTRIBUTE_PROPERTY] = CA_SELECT_GROUP_ATTRIBUTE_NAME
    ca_select_group_attribute[UUID_ATTRIBUTE_PROPERTY] = CA_SELECT_GROUP_ATTRIBUTE_UUID
    ca_select_group_attribute[TYPE_ATTRIBUTE_PROPERTY] = "group"
    ca_select_group_attribute_callback = {
        "callbackContext": "/v1/discoveryProvider/caSelect/{ca_select_method}/{authority_instance_uuid}",
        "callbackMethod": "GET",
        "mappings": [
            {
                "from": "select_ca_method.data",
                "to": "ca_select_method",
                "targets": [
                    "pathVariable"
                ]
            },
            {
                "from": "authority_instance.data.uuid",
                "to": "authority_instance_uuid",
                "targets": [
                    "pathVariable"
                ]
            }
        ]
    }
    ca_select_group_attribute[PROPERTY_ATTRIBUTE_CALLBACK] = ca_select_group_attribute_callback
    return ca_select_group_attribute

################################################################
# Discovery Attributes
################################################################


def get_discovery_info_attribute():
    discovery_info_attribute = dict()
    discovery_info_attribute[NAME_ATTRIBUTE_PROPERTY] = DISCOVERY_INFO_ATTRIBUTE_NAME
    discovery_info_attribute[UUID_ATTRIBUTE_PROPERTY] = DISCOVERY_INFO_ATTRIBUTE_UUID
    discovery_info_attribute[TYPE_ATTRIBUTE_PROPERTY] = "info"
    discovery_info_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "text"
    discovery_info_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = DISCOVERY_INFO_ATTRIBUTE_DESCRIPTION
    discovery_info_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_info_attribute_properties(
        DISCOVERY_INFO_ATTRIBUTE_LABEL,
        is_visible=True)
    markdown_string = """
### Configuration of ADCS certificate discovery

Discovery by default runs on all authorities and templates.
It is looking for all certificates that have disposition >= 12 and <= 21.

If you want to limit the discovery to specific authorities or templates, then select the corresponding values.
    """
    discovery_info_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"data": markdown_string},
    ]
    return discovery_info_attribute


def get_authority_instances_attribute(kind):
    authority_instances = AuthorityInstance.objects.filter(kind=kind)

    authority_instances_attribute = dict()
    authority_instances_attribute[NAME_ATTRIBUTE_PROPERTY] = AUTHORITY_INSTANCE_ATTRIBUTE_NAME
    authority_instances_attribute[UUID_ATTRIBUTE_PROPERTY] = AUTHORITY_INSTANCE_ATTRIBUTE_UUID
    authority_instances_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    authority_instances_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "object"
    authority_instances_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = AUTHORITY_INSTANCE_ATTRIBUTE_DESCRIPTION
    authority_instances_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        AUTHORITY_INSTANCE_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    authority_instances_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": instance.name,
         "data": {
            "uuid": instance.uuid,
            "name": instance.name
         }
         } for instance in authority_instances
    ]
    return authority_instances_attribute


def get_ca_name_attribute(ca_names):
    ca_name_attribute = dict()
    ca_name_attribute[NAME_ATTRIBUTE_PROPERTY] = CA_NAME_ATTRIBUTE_NAME
    ca_name_attribute[UUID_ATTRIBUTE_PROPERTY] = CA_NAME_ATTRIBUTE_UUID
    ca_name_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    ca_name_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "object"
    ca_name_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = CA_NAME_ATTRIBUTE_DESCRIPTION
    ca_name_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        CA_NAME_ATTRIBUTE_LABEL,
        is_required=False,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=True)
    ca_name_attribute[CONTENT_ATTRIBUTE_PROPERTY] = ca_names
    return ca_name_attribute


def get_template_name_attribute():
    template_name_attribute = dict()
    template_name_attribute[NAME_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_ATTRIBUTE_NAME
    template_name_attribute[UUID_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_ATTRIBUTE_UUID
    template_name_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    template_name_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "object"
    template_name_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_ATTRIBUTE_DESCRIPTION
    template_name_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        TEMPLATE_NAME_ATTRIBUTE_LABEL,
        is_required=False,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=True)
    template_name_attribute[PROPERTY_ATTRIBUTE_CALLBACK] = {
        "callbackContext": "/v1/discoveryProvider/listTemplate/{authority_instance_uuid}",
        "callbackMethod": "GET",
        "mappings": [
            {
                "from": "authority_instance.data.uuid",
                "to": "authority_instance_uuid",
                "targets": [
                    "pathVariable"
                ]
            }
        ]
    }
    return template_name_attribute


def get_issued_after_attribute():
    issued_after_attribute = dict()
    issued_after_attribute[NAME_ATTRIBUTE_PROPERTY] = ISSUED_AFTER_ATTRIBUTE_NAME
    issued_after_attribute[UUID_ATTRIBUTE_PROPERTY] = ISSUED_AFTER_ATTRIBUTE_UUID
    issued_after_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    issued_after_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "datetime"
    issued_after_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = ISSUED_AFTER_ATTRIBUTE_DESCRIPTION
    issued_after_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        ISSUED_AFTER_ATTRIBUTE_LABEL,
        is_required=False,
        is_read_only=False,
        is_visible=True,
        is_list=False,
        is_multi_select=False)
    return issued_after_attribute


def get_issued_days_before_attribute():
    issued_days_before_attribute = dict()
    issued_days_before_attribute[NAME_ATTRIBUTE_PROPERTY] = ISSUED_DAYS_BEFORE_ATTRIBUTE_NAME
    issued_days_before_attribute[UUID_ATTRIBUTE_PROPERTY] = ISSUED_DAYS_BEFORE_ATTRIBUTE_UUID
    issued_days_before_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    issued_days_before_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "integer"
    issued_days_before_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = ISSUED_DAYS_BEFORE_ATTRIBUTE_DESCRIPTION
    issued_days_before_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        ISSUED_DAYS_BEFORE_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=False,
        is_multi_select=False)
    issued_days_before_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": "5", "data": "5"},
    ]
    return issued_days_before_attribute

################################################################
# RA Profile Attributes
################################################################


def get_ca_select_group_ra_profile_attribute():
    ca_select_group_ra_profile_attribute = dict()
    ca_select_group_ra_profile_attribute[NAME_ATTRIBUTE_PROPERTY] = CA_SELECT_GROUP_RA_PROFILE_ATTRIBUTE_NAME
    ca_select_group_ra_profile_attribute[UUID_ATTRIBUTE_PROPERTY] = CA_SELECT_GROUP_RA_PROFILE_ATTRIBUTE_UUID
    ca_select_group_ra_profile_attribute[TYPE_ATTRIBUTE_PROPERTY] = "group"
    ca_select_group_ra_profile_attribute_callback = {
        "callbackContext": "/v1/discoveryProvider/caSelect/{ca_select_method}/{authority_instance_uuid}",
        "callbackMethod": "GET",
        "mappings": [
            {
                "from": "select_ca_method.data",
                "to": "ca_select_method",
                "targets": [
                    "pathVariable"
                ]
            },
            {
                "from": "authority_uuid.data",
                "to": "authority_instance_uuid",
                "targets": [
                    "pathVariable"
                ]
            }
        ]
    }
    ca_select_group_ra_profile_attribute[PROPERTY_ATTRIBUTE_CALLBACK] = ca_select_group_ra_profile_attribute_callback
    return ca_select_group_ra_profile_attribute


def get_ca_name_ra_profile_attribute(cas: List[AuthorityData]):
    ca_name_ra_profile_attribute = dict()
    ca_name_ra_profile_attribute[NAME_ATTRIBUTE_PROPERTY] = CA_NAME_RA_PROFILE_ATTRIBUTE_NAME
    ca_name_ra_profile_attribute[UUID_ATTRIBUTE_PROPERTY] = CA_NAME_RA_PROFILE_ATTRIBUTE_UUID
    ca_name_ra_profile_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    ca_name_ra_profile_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "object"
    ca_name_ra_profile_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = CA_NAME_RA_PROFILE_ATTRIBUTE_DESCRIPTION
    ca_name_ra_profile_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        CA_NAME_RA_PROFILE_ATTRIBUTE_LABEL,
        is_required=False,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    ca_name_ra_profile_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": ca.display_name,
         "data": ca.__dict__
         } for ca in cas
    ]
    return ca_name_ra_profile_attribute


def get_authority_uuid_attribute(authority_uuid):
    authority_uuid_attribute = dict()
    authority_uuid_attribute[NAME_ATTRIBUTE_PROPERTY] = AUTHORITY_UUID_ATTRIBUTE_NAME
    authority_uuid_attribute[UUID_ATTRIBUTE_PROPERTY] = AUTHORITY_UUID_ATTRIBUTE_UUID
    authority_uuid_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    authority_uuid_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    authority_uuid_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = AUTHORITY_UUID_ATTRIBUTE_DESCRIPTION
    authority_uuid_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        AUTHORITY_UUID_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=False,
        is_list=False,
        is_multi_select=False)
    authority_uuid_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": authority_uuid, "data": authority_uuid}
    ]
    return authority_uuid_attribute


def get_template_name_ra_profile_attribute(templates: List[TemplateData]):
    template_name_ra_profile_attribute = dict()
    template_name_ra_profile_attribute[NAME_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_NAME
    template_name_ra_profile_attribute[UUID_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_UUID
    template_name_ra_profile_attribute[TYPE_ATTRIBUTE_PROPERTY] = "data"
    template_name_ra_profile_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "object"
    template_name_ra_profile_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_DESCRIPTION
    template_name_ra_profile_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_attribute_properties(
        TEMPLATE_NAME_RA_PROFILE_ATTRIBUTE_LABEL,
        is_required=True,
        is_read_only=False,
        is_visible=True,
        is_list=True,
        is_multi_select=False)
    template_name_ra_profile_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": template.display_name,
         "data": template.__dict__
         } for template in templates
    ]
    return template_name_ra_profile_attribute

################################################################
# Metadata Attributes
################################################################


def get_ca_name_metadata_attribute(ca_name):
    ca_name_metadata_attribute = dict()
    ca_name_metadata_attribute[NAME_ATTRIBUTE_PROPERTY] = CA_NAME_METADATA_ATTRIBUTE_NAME
    ca_name_metadata_attribute[UUID_ATTRIBUTE_PROPERTY] = CA_NAME_METADATA_ATTRIBUTE_UUID
    ca_name_metadata_attribute[TYPE_ATTRIBUTE_PROPERTY] = "meta"
    ca_name_metadata_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    ca_name_metadata_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = CA_NAME_METADATA_ATTRIBUTE_DESCRIPTION
    ca_name_metadata_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_metadata_attribute_properties(
        CA_NAME_METADATA_ATTRIBUTE_LABEL,
        is_visible=True)
    ca_name_metadata_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": ca_name, "data": ca_name}
    ]
    return ca_name_metadata_attribute


def get_template_name_metadata_attribute(template_name):
    template_name_metadata_attribute = dict()
    template_name_metadata_attribute[NAME_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_METADATA_ATTRIBUTE_NAME
    template_name_metadata_attribute[UUID_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_METADATA_ATTRIBUTE_UUID
    template_name_metadata_attribute[TYPE_ATTRIBUTE_PROPERTY] = "meta"
    template_name_metadata_attribute[CONTENT_TYPE_ATTRIBUTE_PROPERTY] = "string"
    template_name_metadata_attribute[DESCRIPTION_ATTRIBUTE_PROPERTY] = TEMPLATE_NAME_METADATA_ATTRIBUTE_DESCRIPTION
    template_name_metadata_attribute[PROPERTY_ATTRIBUTE_PROPERTY] = get_metadata_attribute_properties(
        TEMPLATE_NAME_METADATA_ATTRIBUTE_LABEL,
        is_visible=True)
    template_name_metadata_attribute[CONTENT_ATTRIBUTE_PROPERTY] = [
        {"reference": template_name, "data": template_name}
    ]
    return template_name_metadata_attribute

################################################################
# helper attribute functions
################################################################


def get_attribute_properties(
        label,
        is_read_only=False,
        is_required=True,
        is_list=False,
        is_visible=True,
        is_multi_select=False):
    attribute_properties = dict()
    attribute_properties[LABEL_ATTRIBUTE_PROPERTY] = label
    attribute_properties[READ_ONLY_ATTRIBUTE_PROPERTY] = is_read_only
    attribute_properties[REQUIRED_ATTRIBUTE_PROPERTY] = is_required
    attribute_properties[LIST_ATTRIBUTE_PROPERTY] = is_list
    attribute_properties[VISIBLE_ATTRIBUTE_PROPERTY] = is_visible
    attribute_properties[MUTLISELECT_ATTRIBUTE_PROPERTY] = is_multi_select

    return attribute_properties


def get_info_attribute_properties(
        label,
        is_visible=True,
        group=None):
    attribute_properties = dict()
    attribute_properties[LABEL_ATTRIBUTE_PROPERTY] = label
    attribute_properties[VISIBLE_ATTRIBUTE_PROPERTY] = is_visible
    attribute_properties[GROUP_ATTRIBUTE_PROPERTY] = group

    return attribute_properties


def get_metadata_attribute_properties(
        label,
        is_visible=True,
        group=None,
        is_global=False):
    attribute_properties = dict()
    attribute_properties[LABEL_ATTRIBUTE_PROPERTY] = label
    attribute_properties[VISIBLE_ATTRIBUTE_PROPERTY] = is_visible
    attribute_properties[GROUP_ATTRIBUTE_PROPERTY] = group
    attribute_properties[GLOBAL_ATTRIBUTE_PROPERTY] = is_global

    return attribute_properties
