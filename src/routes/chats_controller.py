import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.chat import Chat
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_chat, validator_find_chats

chat = Blueprint("Chats", __name__)


@chat.route("/chats", methods=["POST"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def add_chat():
    json_values = request.json
    values_required = {"idService", "idMemberATEClient", "idRequest"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_chat.is_valid(json_values):
            chat_add = Chat()
            chat_add.id_service = json_values["idService"]
            chat_add.id_memberATE = json_values["idMemberATEClient"]
            chat_add.id_request = json_values["idRequest"]
            result = chat_add.add_chat()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(chat_add.json_chat()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@chat.route("/chats/<idMember>/<memberType>", methods=["GET"])
@Auth.requires_token
def get_chats(idMember, memberType):
    json_validator = {"idMember": idMember, "memberType": memberType}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_chats.is_valid(json_validator):
        get_chat = Chat()
        get_chat.id_memberATE = idMember
        result = get_chat.find_chats(memberType)
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value \
                or result == ResponsesREST.INVALID_INPUT.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            list_chat = []
            for chats_found in result:
                list_chat.append(chats_found.json_chat())
            response = Response(json.dumps(list_chat), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
