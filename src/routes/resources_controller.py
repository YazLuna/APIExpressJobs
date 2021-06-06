import json

from flask import Blueprint, request, Response

from src.models.resource import Resource
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id, validator_get_resources

resource = Blueprint("Resources", __name__)


@resource.route("/resources", methods=["POST"])
def add_resource():
    resource_save = request.form
    values_required = {"isMainResource", "name", "idService", "idMemberATE"}
    response = response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                                   status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in resource_save for key in values_required):
        # Validator
        resource_add = request.files.getlist("resourceFile")
        if resource_add:
            resource_server = Resource()
            resource_server.is_main_resource = resource_save["isMainResource"]
            resource_server.name = resource_save["name"]
            resource_server.id_service = int(resource_save["idService"])
            resource_server.id_memberATE = int(resource_save["idMemberATE"])
            resource_server.resource_file = resource_add[0]
            result = resource_server.add_resource_server()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(resource_server.json_resource()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@resource.route("/resources/<route>", methods=["DELETE"])
def delete_resource(route):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    resource_delete = Resource()
    resource_delete.route_save = route
    result = resource_delete.delete_resource_server()
    if result == ResponsesREST.SERVER_ERROR.value or result == ResponsesREST.NOT_FOUND.value:
        response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    else:
        response = Response(status=result)
    return response


@resource.route("/resources/<getResource>/<serviceId>", methods=["GET"])
def find_resources(getResource, serviceId):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_get_resources.is_valid({'id': serviceId, 'getResource': getResource}):
        get_resources_service = Resource()
        get_resources_service.id_service = serviceId
        result = get_resources_service.get_resource_list()
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            list_resources = []
            for resource_found in result:
                list_resources.append(resource_found.json_resource())
            response = Response(json.dumps(list_resources), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@resource.route("/resources/<resourceId>", methods=["GET"])
def get_resource_by_id(resourceId):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({'id': resourceId}):
        resource_get = Resource()
        resource_get.id_resource = resourceId
        result = resource_get.get_resource()
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_resource()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
