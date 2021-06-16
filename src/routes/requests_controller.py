"""This module manages the requests."""
import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.request import Request
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id, validator_find_request, \
    validator_change_status_request, validator_request

requestService = Blueprint("Requests", __name__)


@requestService.route("/requests", methods=["POST"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def add_request():
    """This function adds a request from a client."""
    json_values = request.json
    values_required = {"address", "date", "time", "trouble", "idMemberATE", "idService"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_request.validate(json_values):
            request_add = Request()
            request_add.address = json_values["address"]
            request_add.date = json_values["date"]
            request_add.time = json_values["time"]
            request_add.trouble = json_values["trouble"]
            request_add.id_member_ate = json_values["idMemberATE"]
            request_add.id_service = json_values["idService"]
            result = request_add.add_request()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(request_add.json_request()),
                                    status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@requestService.route("/requests/<request_id>", methods=["PATCH"])
@Auth.requires_token
def change_status_request(request_id):
    """This function changes the status of a request."""
    json_values = request.json
    values_required = {"requestStatus"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idRequest"] = request_id
        if validator_change_status_request.is_valid(json_validator):
            request_change_status = Request()
            request_change_status.id_request = request_id
            request_change_status.request_status = json_values["requestStatus"]
            result = request_change_status.change_status()
            if result in (ResponsesREST.SERVER_ERROR.value, ResponsesREST.INVALID_INPUT.value):
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
            else:
                response = Response(status=result)
    return response


@requestService.route("/requests/<request_status>/<filter_search>/<criterion>", methods=["GET"])
@Auth.requires_token
def find_requests(request_status, filter_search, criterion):
    """This function retrieves the list of requests from the service or memberATE criterion."""
    json_validator = {"requestStatus": request_status,
                      "filterSearch": filter_search, "criterion": criterion}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_request.is_valid(json_validator):
        get_request = Request()
        result = get_request.find_request(request_status, filter_search, criterion)
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value,
                      ResponsesREST.INVALID_INPUT.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_requests = []
            for request_found in result:
                list_requests.append(request_found.json_request())
            response = Response(json.dumps(list_requests),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@requestService.route("/requests/<request_id>", methods=["GET"])
@Auth.requires_token
def get_request_by_id(request_id):
    """This function retrieves a request according to its ID."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": request_id}):
        request_get = Request()
        request_get.id_request = request_id
        result = request_get.get_request_by_id()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_request()),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@requestService.route("/requests/services/<service_id>", methods=["GET"])
@Auth.requires_token
def find_requests_service(service_id):
    """This function retrieves the list of requests from the service."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": service_id}):
        get_request = Request()
        result = get_request.find_request_service(service_id)
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value,
                      ResponsesREST.INVALID_INPUT.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_requests = []
            for request_found in result:
                list_requests.append(request_found.json_request())
            response = Response(json.dumps(list_requests),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
