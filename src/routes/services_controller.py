import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.service import Service
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id, validator_find_services, validator_change_status_service, \
    validator_service

service = Blueprint("Services", __name__)


@service.route("/services", methods=["POST"])
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
@Auth.requires_token
def add_service():
    json_values = request.json
    values_required = {"name", "description", "slogan", "typeService", "workingHours",
                       "minimalCost", "maximumCost", "idCity", "idMemberATE"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_service.is_valid(json_values):
            service_add = Service()
            service_add.name = json_values["name"]
            service_add.description = json_values["description"]
            service_add.slogan = json_values["slogan"]
            service_add.type_service = json_values["typeService"]
            service_add.working_hours = json_values["workingHours"]
            service_add.minimal_cost = json_values["minimalCost"]
            service_add.maximum_cost = json_values["maximumCost"]
            service_add.id_city = json_values["idCity"]
            service_add.id_memberATE = json_values["idMemberATE"]
            result = service_add.add_service()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(service_add.json_service()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@service.route("/services/<serviceId>", methods=["PUT"])
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
@Auth.requires_token
def change_service(serviceId):
    json_values = request.json
    values_required = {"name", "description", "slogan", "typeService", "workingHours",
                       "minimalCost", "maximumCost", "idCity", "idMemberATE"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idService"] = serviceId
        if validator_service.is_valid(json_validator):
            service_change = Service()
            service_change.id_service = serviceId
            service_change.name = json_values["name"]
            service_change.description = json_values["description"]
            service_change.slogan = json_values["slogan"]
            service_change.type_service = json_values["typeService"]
            service_change.working_hours = json_values["workingHours"]
            service_change.minimal_cost = json_values["minimalCost"]
            service_change.maximum_cost = json_values["maximumCost"]
            service_change.id_city = json_values["idCity"]
            service_change.id_memberATE = json_values["idMemberATE"]
            result = service_change.change_service()
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(json.dumps(service_change.json_service()), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(result), status=result, mimetype="application/json")
    return response


@service.route("/services/<idService>", methods=["PATCH"])
@Auth.requires_token
def change_status(idService):
    json_values = request.json
    values_required = {"serviceStatus"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idService"] = idService
        if validator_change_status_service.is_valid(json_validator):
            service_change_status = Service()
            service_change_status.id_service = idService
            service_change_status.service_status = json_values["serviceStatus"]
            result = service_change_status.change_status()
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(status=result)
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@service.route("/services/<serviceStatus>/<filterSearch>/<criterion>", methods=["GET"])
@Auth.requires_token
def find_services(serviceStatus, filterSearch, criterion):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_services.is_valid(
            {"serviceStatus": serviceStatus, "filterSearch": filterSearch, "criterion": criterion}):
        get_services = Service()
        result = get_services.consult_list_services(serviceStatus, filterSearch, criterion)
        if result == ResponsesREST.INVALID_INPUT.value or result == ResponsesREST.SERVER_ERROR.value \
                or result == ResponsesREST.NOT_FOUND.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            list_services = []
            for service_found in result:
                list_services.append(service_found.json_service())
            response = Response(json.dumps(list_services), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@service.route("/services/<serviceId>", methods=["GET"])
@Auth.requires_token
def get_service_by_id(serviceId):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": serviceId}):
        service_get = Service()
        service_get.id_service = serviceId
        result = service_get.consult_service()
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_service()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
