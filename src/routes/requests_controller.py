import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.request import Request
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

requestService = Blueprint("Requests", __name__)


@requestService.route("/requests", methods=["POST"])
@Auth.requires_role(AccountRole.CLIENT.name)
@Auth.requires_token
def add_request():
    json_values = request.json
    values_required = {"address", "date", "time", "trouble", "idMemberATE", "idService"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        request_add = Request()
        request_add.address = json_values["address"]
        request_add.date = json_values["date"]
        request_add.time = json_values["time"]
        request_add.trouble = json_values["trouble"]
        request_add.service_status = json_values["serviceStatus"]
        request_add.id_memberATE = json_values["idMemberATE"]
        request_add.id_service = json_values["idService"]
        result = request_add.add_request()
        if result == ResponsesREST.CREATED.value:
            response = Response(json.dumps(request_add.json_request()), status=ResponsesREST.CREATED.value,
                                mimetype="application/json")
        else:
            response = Response(status=result)
    return response


@requestService.route("/requests/<requestId>", methods=["PATCH"])
@Auth.requires_token
def change_status_request(requestId):
    json_values = request.json
    values_required = {"requestStatus"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        request_change_status = Request()
        request_change_status.id_request = requestId
        request_change_status.request_status = json_values["requestStatus"]
        result = request_change_status.change_status()
        response = Response(status=result)
    return response


@requestService.route("/requests", methods=["GET"])
@Auth.requires_token
def find_requests():
    json_values = request.json
    values_required = {"requestStatus", "filter", "criterion"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        get_request = Request()
        result = get_request.find_request(json_values["requestStatus"], json_values["filter"],
                                          json_values["criterion"])
        if result == ResponsesREST.INVALID_REQUEST.value:
            response = Response(status=result)
        else:
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(status=result)
            else:
                list_requests = []
                for request_found in result:
                    request_found.json_request()
                    list_requests.append(request_found)
                response = Response(json.dumps(list_requests), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
    return response


@requestService.route("/requests/<requestId>", methods=["POST"])
@Auth.requires_token
def get_request_by_id(requestId):
    request_get = Request()
    request_get.id_request = requestId
    result = request_get.get_request_by_id()
    if result == ResponsesREST.INVALID_INPUT.value:
        response = Response(status=result)
    else:
        if result == ResponsesREST.SERVER_ERROR.value:
            response = Response(status=result)
        else:
            response = Response(json.dumps(result.json_request()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
