"""This module manage the logins."""
import json

from flask import Blueprint, request, Response, session

from src.models.account import Account
from src.models.account_role import AccountRole
from src.models.account_status import AccountStatus
from src.models.password import encode_password
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_login, validator_login_validator, \
    validator_login_password

login = Blueprint("Logins", __name__)


@login.route("/logins", methods=["POST"])
def create_token():
    """This function logs in and generates the access token."""
    json_values = request.json
    values_required = {"username", "password"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_login.is_valid(json_values):
            account_login = Account()
            account_login.username = json_values["username"]
            account_login.password = encode_password(json_values["password"])
            account_login.member_ate_status = AccountStatus.ACTIVE.value
            result = account_login.login()
            if result in (ResponsesREST.SERVER_ERROR.value, ResponsesREST.NOT_FOUND.value,
                          ResponsesREST.INVALID_REQUEST.value):
                response = Response(json.dumps(json_error(result)),
                                    status=result,
                                    mimetype="application/json")
            else:
                account_login.member_ate_type = result.member_ate_type
                account_login.id_member_ate = result.id_member_ate
                account_login.id_city = result.id_city
                token = Auth.generate_token(account_login)
                session.permanent = True
                session["token"] = token
                response = Response(json.dumps({"token": token,
                                                "memberATEType": account_login.member_ate_type,
                                                "idMemberATE": account_login.id_member_ate,
                                                "idCity": account_login.id_city}),
                                    status=ResponsesREST.CREATED.value, mimetype="application/json")
    return response


@login.route("/logins", methods=["PATCH"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT_EMPLOYEE.name)
def update_token():
    """This function changes an employee's token so that he can sign in as a client."""
    json_values = request.json
    values_required = {"username", "password"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_login.is_valid(json_values):
            account_login = Account()
            account_login.username = json_values["username"]
            account_login.password = encode_password(json_values["password"])
            token = Auth.generate_token(account_login)
            session.permanent = True
            session["token"] = token
            response = Response(json.dumps({"token": token}),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@login.route("/logins/validator", methods=["PATCH"])
def validate_account():
    """This function validates an account so that you can log in."""
    json_values = request.json
    values_required = {"username", "password", "code"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_login_validator.is_valid(json_values):
            account_login = Account()
            account_login.username = json_values["username"]
            account_login.password = encode_password(json_values["password"])
            result = account_login.validate_account(json_values["code"])
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(status=result)
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@login.route("/logins/validatePassword", methods=["PATCH"])
def validate_change_password():
    """This function changes the password of an account based on the
     confirmation code."""
    json_values = request.json
    values_required = {"email", "password", "code"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_login_password.is_valid(json_values):
            account_login = Account()
            account_login.email = json_values["email"]
            account_login.password = encode_password(json_values["password"])
            result = account_login.validate_change_password(json_values["code"])
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(status=result)
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response
