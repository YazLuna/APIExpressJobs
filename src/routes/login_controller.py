import json

from flask import Blueprint, request, Response, session

from src.models.account import Account
from src.models.account_role import AccountRole
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_login

login = Blueprint("Logins", __name__)


@login.route("/logins", methods=["POST"])
def create_token():
    json_values = request.json
    values_required = {"username", "password"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_login.is_valid(json_values):
            account_login = Account()
            account_login.username = json_values["username"]
            account_login.password = json_values["password"]
            result = account_login.login()
            if result is False:
                response = Response(json.dumps(json_error(ResponsesREST.NOT_FOUND.value)), status=request,
                                    mimetype="application/json")
            else:
                account_login.memberATE_type = result.memberATE_type
                account_login.id_memberATE = result.id_memberATE
                token = Auth.generate_token(account_login)
                session.permanent = True
                session["token"] = token
                response = Response(json.dumps({"token": token, "memberATEType": account_login.memberATE_type,
                                                "idMemberATE": account_login.id_memberATE}),
                                    status=ResponsesREST.CREATED.value, mimetype="application/json")
    return response


@login.route("/logins", methods=["PATCH"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
def update_token():
    json_values = request.json
    values_required = {"username", "password"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_login.is_valid(json_values):
            account_login = Account()
            account_login.username = json_values["username"]
            account_login.password = json_values["password"]
            token = Auth.generate_token(account_login)
            session.permanent = True
            session["token"] = token
            response = Response(json.dumps({"token": token}), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
