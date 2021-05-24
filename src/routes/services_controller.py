import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.service import Service
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

service = Blueprint("Services", __name__)


@service.route("/services", methods=["POST"])
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
@Auth.requires_token
def add_service():
    json_values = request.json
    values_required = {"name", "description", "slogan", "typeService", "workingHours",
                       "serviceStatus", "minimalCost", "maximumCost", "idCity", "idMemberATE"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        service_add = Service()
        service_add.name = json_values["name"]
        service_add.description = json_values["description"]
        service_add.slogan = json_values["slogan"]
        service_add.type_service = json_values["typeService"]
        service_add.working_hours = json_values["workingHours"]
        service_add.service_status = json_values["serviceStatus"]
        service_add.minimal_cost = json_values["minimalCost"]
        service_add.maximum_cost = json_values["maximumCost"]
        service_add.id_city = json_values["idCity"]
        service_add.id_memberATE = json_values["idMemberATE"]
        result = service_add.add_service()
        if result == ResponsesREST.CREATED.value:
            response = Response(json.dumps(service_add.json_service()), status=ResponsesREST.CREATED.value,
                                mimetype="application/json")
        else:
            response = Response(status=result)
    return response


@service.route("/services/<serviceId>", methods=["PUT"])
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
@Auth.requires_token
def change_service(serviceId):
    json_values = request.json
    values_required = {"name", "description", "slogan", "typeService", "workingHours",
                       "minimalCost", "maximumCost", "idCity", "idMemberATE"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
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
            response = Response(status=result)
    return response


@service.route("/services/<idService>", methods=["PATCH"])
@Auth.requires_token
def change_status(idService):
    json_values = request.json
    values_required = {"serviceStatus"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        service_change_status = Service()
        service_change_status.id_service = idService
        service_change_status.service_status = json_values["serviceStatus"]
        result = service_change_status.change_status()
        response = Response(status=result)
    return response


@service.route("/services", methods=["GET"])
@Auth.requires_token
def find_services():
    json_values = request.json
    values_required = {"serviceStatus", "filter", "criterion"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        get_services = Service()
        result = get_services.consult_list_services(json_values["serviceStatus"], json_values["filter"],
                                                    json_values["criterion"])
        if result == ResponsesREST.INVALID_REQUEST.value:
            response = Response(status=result)
        else:
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(status=result)
            else:
                list_services = []
                for service_found in result:
                    service_found.json_account()
                    list_services.append(service_found)
                response = Response(json.dumps(list_services), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
    return response


@service.route("/services/<serviceId>", methods=["GET"])
@Auth.requires_token
def get_service_by_id(serviceId):
    service_get = Service()
    service_get.id_service = serviceId
    result = service_get.consult_service()
    if result == ResponsesREST.INVALID_INPUT.value:
        response = Response(status=result)
    else:
        if result == ResponsesREST.SERVER_ERROR.value:
            response = Response(status=result)
        else:
            response = Response(json.dumps(result.json_service()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
