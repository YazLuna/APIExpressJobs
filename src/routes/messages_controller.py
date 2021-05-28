import json

from flask import Blueprint, request, Response

from src.models.message import Message
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id_json, validator_message

message = Blueprint("Messages", __name__)


@message.route("/messages", methods=["POST"])
@Auth.requires_token
def add_message():
    json_values = request.json
    values_required = {"message", "idChat", "memberATEType"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_message.is_valid(json_values):
            message_add = Message()
            message_add.message = json_values["message"]
            message_add.id_chat = json_values["idChat"]
            message_add.memberType = json_values["memberType"]
            result = message_add.add_message()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(message_add.json_message()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@message.route("/messages", methods=["GET"])
@Auth.requires_token
def get_messages():
    json_values = request.json
    values_required = {"idChat"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_id_json.is_valid(json_values):
            get_message = Message()
            get_message.id_chat = json_values["idChat"]
            result = get_message.get_messages_list()
            if result == ResponsesREST.INVALID_REQUEST.value:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
            else:
                if result == ResponsesREST.SERVER_ERROR.value:
                    response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
                else:
                    list_chat = []
                    for message_found in result:
                        message_found.json_message()
                        list_chat.append(message_found)
                    response = Response(json.dumps(list_chat), status=ResponsesREST.SUCCESSFUL.value,
                                        mimetype="application/json")
    return response
