import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from PyADCSConnector.remoting.winrm.scripts import get_cas_script, get_templates_script
from PyADCSConnector.remoting.winrm_remoting import create_session_from_authority_instance_name, \
    create_session_from_authority_instance_uuid
from PyADCSConnector.utils.dump_parser import DumpParser
from PyADCSConnector.views.attributes import get_winrm_transport_configuration_attributes_list


@require_http_methods(["GET"])
def get_winrm_transport_configuration(request, kind, wirm_transport, *args, **kwargs):
    json.loads(request.body)
    return JsonResponse(get_winrm_transport_configuration_attributes_list(kind, wirm_transport), safe=False,
                        content_type="application/json")


@require_http_methods(["GET"])
def get_ca_names(request, authority_instance_uuid, *args, **kwargs):
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

    return JsonResponse(content, safe=False,
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


def remove_headers(result):
    input_string = result.std_out.decode('utf-8')
    lines = input_string.strip().split('\n')

    # Remove first 2 lines as header
    lines = lines[2:]

    # Remove blank lines
    lines = [line for line in lines if line.strip()]

    # Trim end
    lines = [line.rstrip() for line in lines]

    # Join the cleaned lines back into a string
    # cleaned_string = '\n'.join(lines)

    # Return CAs each on one line
    return lines
