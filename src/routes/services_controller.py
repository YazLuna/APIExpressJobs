"""This module manages the services."""
import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.service import Service
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id, validator_find_services, \
    validator_change_status_service, validator_service, validator_find_services_city

service = Blueprint("Services", __name__)


@service.route("/services", methods=["POST"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
def add_service():
    """This function adds a service."""
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
            service_add.id_member_ate = json_values["idMemberATE"]
            result = service_add.add_service()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(service_add.json_service()),
                                    status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@service.route("/services/<service_id>", methods=["PUT"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
def change_service(service_id):
    """This function changes all the data of a service according to its ID."""
    json_values = request.json
    values_required = {"name", "description", "slogan", "typeService", "workingHours",
                       "minimalCost", "maximumCost", "idCity", "idMemberATE"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idService"] = int(service_id)
        if validator_service.is_valid(json_validator):
            service_change = Service()
            service_change.id_service = int(service_id)
            service_change.name = json_values["name"]
            service_change.description = json_values["description"]
            service_change.slogan = json_values["slogan"]
            service_change.type_service = json_values["typeService"]
            service_change.working_hours = json_values["workingHours"]
            service_change.minimal_cost = json_values["minimalCost"]
            service_change.maximum_cost = json_values["maximumCost"]
            service_change.id_city = json_values["idCity"]
            service_change.id_member_ate = int(json_values["idMemberATE"])
            result = service_change.change_service()
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(json.dumps(service_change.json_service()),
                                    status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@service.route("/services/<service_id>", methods=["PATCH"])
@Auth.requires_token
def change_status(service_id):
    """This function changes the status of a service, 1 active, 2 inactive, 3 blocked."""
    json_values = request.json
    values_required = {"serviceStatus"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idService"] = service_id
        if validator_change_status_service.is_valid(json_validator):
            service_change_status = Service()
            service_change_status.id_service = service_id
            service_change_status.service_status = json_values["serviceStatus"]
            result = service_change_status.change_status()
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(status=result)
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@service.route("/services/<service_status>/<filter_search>/<criterion>", methods=["GET"])
@Auth.requires_token
def find_services_manager(service_status, filter_search, criterion):
    """This function obtains the list of services according to one of the following criteria:
     typeService, name, minimalCost or maximumCost."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_services.is_valid(
            {"serviceStatus": service_status, "filterSearch": filter_search,
             "criterion": criterion}):
        get_services = Service()
        result = get_services.consult_list_services(service_status, filter_search, criterion)
        if result in (ResponsesREST.INVALID_INPUT.value, ResponsesREST.SERVER_ERROR.value,
                      ResponsesREST.NOT_FOUND.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_services = []
            for service_found in result:
                list_services.append(service_found.json_service())
            response = Response(json.dumps(list_services),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@service.route("/services/city/<id_city>", methods=["GET"])
@Auth.requires_token
def find_services_city(id_city):
    """This function gets the list of services for a city."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": id_city}):
        get_services = Service()
        get_services.id_city = id_city
        result = get_services.get_services_city()
        if result in (ResponsesREST.SERVER_ERROR.value, ResponsesREST.NOT_FOUND.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_services = []
            for service_found in result:
                list_services.append(service_found.json_service())
            response = Response(json.dumps(list_services),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@service.route("/services/employee/<id_member_ate>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
def find_services_employee(id_member_ate):
    """This function gets the list of services for an employee."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": id_member_ate}):
        get_services = Service()
        get_services.id_member_ate = id_member_ate
        result = get_services.get_services_employee()
        if result in (ResponsesREST.SERVER_ERROR.value, ResponsesREST.NOT_FOUND.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_services = []
            for service_found in result:
                list_services.append(service_found.json_service())
            response = Response(json.dumps(list_services),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@service.route("/services/city/<filter_search>/<criterion>/<id_city>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def find_services_city_filter(filter_search, criterion, id_city):
    """This function obtains the list of services of a city according to the following criteria:
    typeService, name, minimalCost or maximumCost."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_services_city.is_valid(
            {"filterSearch": filter_search, "criterion": criterion, "idCity": id_city}):
        get_services = Service()
        get_services.id_city = id_city
        result = get_services.consult_list_services_city(filter_search, criterion)
        if result in (ResponsesREST.INVALID_INPUT.value, ResponsesREST.SERVER_ERROR.value,
                      ResponsesREST.NOT_FOUND.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_services = []
            for service_found in result:
                list_services.append(service_found.json_service())
            response = Response(json.dumps(list_services),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@service.route("/services/<service_id>", methods=["GET"])
@Auth.requires_token
def get_service_by_id(service_id):
    """This function gets a service according to its ID."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": service_id}):
        service_get = Service()
        service_get.id_service = service_id
        result = service_get.consult_service()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_service()),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
