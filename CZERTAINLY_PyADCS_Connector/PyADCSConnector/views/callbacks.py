from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from PyADCSConnector.remoting.winrm.scripts import get_cas_script, get_templates_script
from PyADCSConnector.remoting.winrm_remoting import create_session_from_authority_instance_uuid
from PyADCSConnector.services.attributes.authority_attributes import get_winrm_transport_configuration_attributes_list
from PyADCSConnector.services.attributes.discovery_attributes import get_discovery_config_string_attribute, \
    get_discovery_ca_name_attribute
from PyADCSConnector.services.attributes.raprofile_attributes import get_raprofile_config_string_attribute, \
    get_raprofile_ca_name_attribute
from PyADCSConnector.utils.ca_select_method import CaSelectMethod
from PyADCSConnector.utils.dump_parser import DumpParser


@require_http_methods(["GET"])
def get_winrm_transport_configuration(request, kind, wirm_transport):
    return JsonResponse(get_winrm_transport_configuration_attributes_list(kind, wirm_transport), safe=False,
                        content_type="application/json")


@require_http_methods(["GET"])
def get_discovery_ca_select_configuration(request, ca_select_method: str, authority_instance_uuid: str, *args, **kwargs):
    attributes = []
    if ca_select_method == CaSelectMethod.CONFIGSTRING.method:
        attributes.append(get_discovery_config_string_attribute())
    elif ca_select_method == CaSelectMethod.SEARCH.method:
        attributes.append(get_discovery_ca_name_attribute(get_ca_names_service(authority_instance_uuid)))
    else:
        raise Exception("Unknown CA Select Method: " + ca_select_method)

    return JsonResponse(attributes, safe=False,content_type="application/json")


@require_http_methods(["GET"])
def get_raprofile_ca_select_configuration(request, ca_select_method: str, authority_instance_uuid: str, *args, **kwargs):
    attributes = []
    if ca_select_method == CaSelectMethod.CONFIGSTRING.method:
        attributes.append(get_raprofile_config_string_attribute())
    elif ca_select_method == CaSelectMethod.SEARCH.method:
        attributes.append(get_raprofile_ca_name_attribute(get_ca_names_service(authority_instance_uuid)))
    else:
        raise Exception("Unknown CA Select Method: " + ca_select_method)

    return JsonResponse(attributes, safe=False,content_type="application/json")


@require_http_methods(["GET"])
def get_ca_names(request, authority_instance_uuid, *args, **kwargs):
    return JsonResponse(get_ca_names_service(authority_instance_uuid), safe=False,
                        content_type="application/json")


@require_http_methods(["GET"])
def get_template_names(request, authority_instance_uuid, *args, **kwargs):
    session = create_session_from_authority_instance_uuid(authority_instance_uuid)
    session.connect()
    result = session.run_ps(get_templates_script())
    session.disconnect()

    # Convert string to lines
    # regular_string = result.std_out.decode('utf-8')
    templates = DumpParser.parse_template_data(result)

    content = [
        {"reference": template.display_name,
         "data": {
             "name": template.name,
             "display_name": template.display_name,
             "schema_version": template.schema_version,
             "version": template.version,
             "oid": template.oid
         }
         } for template in templates
    ]

    return JsonResponse(content, safe=False,
                        content_type="application/json")


def get_ca_names_service(authority_instance_uuid):
    session = create_session_from_authority_instance_uuid(authority_instance_uuid)
    session.connect()
    result = session.run_ps(get_cas_script())
    session.disconnect()

    # Convert string to lines
    # regular_string = result.std_out.decode('utf-8')
    cas = DumpParser.parse_authority_data(result)

    content = [
        {"reference": ca.display_name,
         "data": {
             "name": ca.name,
             "display_name": ca.display_name,
             "computer_name": ca.computer_name,
             "config_string": ca.config_string,
             "ca_type": ca.ca_type,
             "is_enterprise": ca.is_enterprise,
             "is_root": ca.is_root
         }
         } for ca in cas
    ]

    return content