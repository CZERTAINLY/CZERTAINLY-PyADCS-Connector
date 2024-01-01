import json

from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from PyADCSConnector.exceptions.remoting_exception import RemotingException
from PyADCSConnector.models.authority_instance import AuthorityInstance
from PyADCSConnector.remoting.winrm.scripts import verify_connection_script
from PyADCSConnector.remoting.winrm_remoting import WinRmRemoting
from PyADCSConnector.serializers.authority_instance_serializer import AuthorityInstanceSerializer
from PyADCSConnector.utils import attribute_definition_utils
from PyADCSConnector.views.attributes import get_attributes_list, get_winrm_transport_configuration_attributes_list, \
    get_all_attributes_list
from PyADCSConnector.views.constants import *


class AuthorityInstanceAttributeObject:
    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid

    @staticmethod
    def from_dict(authority_instance_dict):
        return AuthorityInstanceAttributeObject(
            authority_instance_dict["name"],
            authority_instance_dict["uuid"])

    @staticmethod
    def from_dicts(authority_instance_dicts):
        return [AuthorityInstanceAttributeObject.from_dict(authority_instance_dict)
                for authority_instance_dict in authority_instance_dicts]


@require_http_methods(["GET", "POST"])
@transaction.atomic
def authority_operations(request):
    if request.method == "GET":
        authorities = AuthorityInstance.objects
        serializer = AuthorityInstanceSerializer(authorities, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return create_authority_instance(request)


@require_http_methods(["GET", "POST", "DELETE"])
@transaction.atomic
def authority_instance_operations(request, uuid, *args, **kwargs):
    if request.method == "GET":
        try:
            authority = AuthorityInstance.objects.get(uuid=uuid)
            serializer = AuthorityInstanceSerializer(authority)
            return JsonResponse(serializer.data, safe=False)
        except AuthorityInstance.DoesNotExist as e:
            return JsonResponse({"message": "Requested Authority with UUID %s not found" % uuid}, status=404)
    elif request.method == "DELETE":
        try:
            AuthorityInstance.objects.get(uuid=uuid).delete()
            return HttpResponse(status=204)
        except AuthorityInstance.DoesNotExist as e:
            return JsonResponse({"message": "Requested Authority with UUID %s not found" % uuid}, status=404)
    elif request.method == "POST":
        try:
            authority = AuthorityInstance.objects.get(uuid=uuid)
            return update_authority_instance(request, authority)
        except AuthorityInstance.DoesNotExist as e:
            return JsonResponse({"message": "Requested Authority with UUID %s not found" % uuid}, status=404)
    else:
        raise ValueError("Update authority is not supported")


def create_authority_instance(request):
    form = json.loads(request.body)

    if AuthorityInstance.objects.filter(name=form["name"]).exists():
        return JsonResponse({"message": "Authority instance with name %s already exists" % form["name"]}, status=400)

    authority_instance: AuthorityInstance = AuthorityInstance()
    authority_instance.name = form["name"]
    authority_instance.kind = form["kind"]

    return update_authority_instance(request, authority_instance)


def update_authority_instance(request, authority_instance):
    if authority_instance.kind != "PyADCS-WinRM":
        raise ValueError("Unrecognized kind: %s" % authority_instance.kind)

    form = json.loads(request.body)

    request_attributes = form["attributes"]
    authority_instance.transport = attribute_definition_utils.get_attribute_value(WINRM_TRANSPORT_ATTRIBUTE_NAME,
                                                                                 request_attributes)
    # original_attributes = (get_winrm_transport_configuration_attributes_list(authority_instance.kind, authority_instance.transport) +
    #                        get_attributes_list(authority_instance.kind))
    original_attributes = get_all_attributes_list(authority_instance.kind, authority_instance.transport)
    authority_instance.attributes = attribute_definition_utils.merge_attributes(request_attributes, original_attributes)
    authority_instance.address = attribute_definition_utils.get_attribute_value(SERVER_ADDRESS_ATTRIBUTE_NAME,
                                                                                authority_instance.attributes)
    authority_instance.https = attribute_definition_utils.get_attribute_value(USE_HTTPS_ATTRIBUTE_NAME,
                                                                                  authority_instance.attributes)
    authority_instance.port = attribute_definition_utils.get_attribute_value(WINRM_PORT_ATTRIBUTE_NAME,
                                                                             authority_instance.attributes)
    authority_instance.credential = attribute_definition_utils.get_attribute_value(CREDENTIAL_ATTRIBUTE_NAME,
                                                                                   authority_instance.attributes)

    try:
        verify_connection(authority_instance)
    except RemotingException as e:
        return JsonResponse({"message": "Connection to ADCS server failed: %s" % str(e)}, status=400)

    authority_instance.save()

    serializer = AuthorityInstanceSerializer(authority_instance)
    return JsonResponse(serializer.data)


def verify_connection(authority_instance):
    username = attribute_definition_utils.get_attribute_value("username",
                                                              authority_instance.credential.get("attributes"))
    password = attribute_definition_utils.get_attribute_value("password",
                                                              authority_instance.credential.get("attributes"))

    if authority_instance.transport == "credssp":
        session = WinRmRemoting(username, password, authority_instance.address, authority_instance.https,
                                authority_instance.port)
        session.connect()
        result = session.run_ps(verify_connection_script())
        session.disconnect()
        if result.status_code != 0:
            raise RemotingException("Failed to connect to ADCS server: %s" % result.std_err)
    else:
        raise RemotingException("Unsupported transport type: %s" % authority_instance.transport)
