import json

from flask import Blueprint, request, Response

from src.models.chat import Chat
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

chat = Blueprint("Chats", __name__)


@chat.route("/chats", methods=["POST"])
@Auth.requires_token
def add_chat():
    json_values = request.json
    values_required = {"idService", "idMemberATEClient", "idRequest"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        chat_add = Chat()
        chat_add.id_service = json_values["isService"]
        chat_add.id_memberATE = json_values["idMemberATEClient"]
        chat_add.id_request = json_values["idRequest"]
        result = chat_add.add_chat()
        if result == ResponsesREST.CREATED.value:
            response = Response(json.dumps(chat_add.json_chat()), status=ResponsesREST.CREATED.value,
                                mimetype="application/json")
        else:
            response = Response(status=result)
    return response


@chat.route("/chats", methods=["GET"])
@Auth.requires_token
def get_chats():
    json_values = request.json
    values_required = {"idMember"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        get_chat = Chat()
        get_chat.id_memberATE = json_values["idMember"]
        result = get_chat.find_chats()
        if result == ResponsesREST.INVALID_REQUEST.value:
            response = Response(status=result)
        else:
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(status=result)
            else:
                list_chat = []
                for chats_found in result:
                    chats_found.json_chat()
                    list_chat.append(chats_found)
                response = Response(json.dumps(list_chat), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
    return response
