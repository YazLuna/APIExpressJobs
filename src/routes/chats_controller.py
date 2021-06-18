"""This module manages the chats of the membersATE."""
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
    """This function adds a chat to the database."""
    json_values = request.json
    values_required = {"idService", "idMemberATE", "idRequest"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_chat.is_valid(json_values):
            chat_add = Chat()
            chat_add.id_service = json_values["idService"]
            chat_add.id_member_ate = json_values["idMemberATEClient"]
            chat_add.id_request = json_values["idRequest"]
            result = chat_add.add_chat()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(chat_add.json_chat()),
                                    status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@chat.route("/chats/<id_member>/<member_type>", methods=["GET"])
@Auth.requires_token
def get_chats(id_member, member_type):
    """This function fetches a memberATE's chats."""
    json_validator = {"idMember": id_member, "memberType": member_type}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_chats.is_valid(json_validator):
        get_chat = Chat()
        get_chat.id_member_ate = id_member
        result = get_chat.find_chats(member_type)
        if result in (ResponsesREST.NOT_FOUND.value,
                      ResponsesREST.SERVER_ERROR.value, ResponsesREST.INVALID_INPUT.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_chat = []
            for chats_found in result:
                list_chat.append(chats_found.json_chat())
            response = Response(json.dumps(list_chat),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
