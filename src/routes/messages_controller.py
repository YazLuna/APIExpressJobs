"""This module manage the messages."""
import json

from flask import Blueprint, request, Response

from src.models.message import Message
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_message, validator_id

message = Blueprint("Messages", __name__)


@message.route("/messages", methods=["POST"])
@Auth.requires_token
def add_message():
    """This function add a message to chat."""
    json_values = request.json
    values_required = {"message", "idChat", "memberATEType"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_message.is_valid(json_values):
            message_add = Message()
            message_add.message = json_values["message"]
            message_add.id_chat = json_values["idChat"]
            message_add.member_type = json_values["memberATEType"]
            result = message_add.add_message()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(message_add.json_message()),
                                    status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@message.route("/messages/<id_chat>", methods=["GET"])
@Auth.requires_token
def get_messages(id_chat):
    """This function get a messages from a chat."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": id_chat}):
        get_message = Message()
        get_message.id_chat = id_chat
        result = get_message.get_messages_list()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_chat = []
            for message_found in result:
                list_chat.append(message_found.json_message())
            response = Response(json.dumps(list_chat),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
