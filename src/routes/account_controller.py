"""This module manages memberATE accounts."""
import json

from flask import Blueprint, request, Response

from src.models.account import Account
from src.models.account_role import AccountRole
from src.models.password import encode_password
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_memberATE, validator_change_status_member, \
    validator_find_accounts, validator_id, validator_memberATE_change, validator_memberATE_password

account = Blueprint("Accounts", __name__)


@account.route("/accounts", methods=["POST"])
def add_account():
    """This function adds an account and sends the verification code to the email address."""
    json_values = request.json
    values_required = {"username", "password", "name", "lastname", "dateBirth",
                       "email", "idCity"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_memberATE.is_valid(json_values):
            account_add = Account()
            account_add.username = json_values["username"]
            account_add.password = encode_password(json_values["password"])
            account_add.name = json_values["name"]
            account_add.lastname = json_values["lastname"]
            account_add.date_birth = json_values["dateBirth"]
            account_add.email = json_values["email"]
            account_add.id_city = json_values["idCity"]
            result = account_add.add_member_ate()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(account_add.json_account()),
                                    status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result,
                                    mimetype="application/json")
    return response


@account.route("/accounts/<account_id>", methods=["PATCH"])
@Auth.requires_token
def change_status_account(account_id):
    """This feature changes the status of an account based on its ID."""
    json_values = request.json
    values_required = {"memberATEStatus"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idAccount"] = account_id
        if validator_change_status_member.is_valid(json_validator):
            account_status = Account()
            account_status.id_member_ate = account_id
            account_status.member_ate_status = json_values["memberATEStatus"]
            result = account_status.change_status()
            if result in (ResponsesREST.SERVER_ERROR.value,
                          ResponsesREST.INVALID_INPUT.value):
                response = Response(json.dumps(json_error(result)),
                                    status=result,
                                    mimetype="application/json")
            else:
                response = Response(status=result)
    return response


@account.route("/accounts/<filter_search>/<criterion>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.MANAGER.name)
def find_accounts(filter_search, criterion):
    """This function searches for accounts based on one of the following criteria:
    first name, last name, email or status."""
    json_validator = {"filterSearch": filter_search, "criterion": criterion}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_accounts.is_valid(json_validator):
        get_accounts = Account()
        result = get_accounts.consult_list_accounts(filter_search, criterion)
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value,
                      ResponsesREST.INVALID_INPUT.value):
            response = Response(json.dumps(json_error(result)), status=result,
                                mimetype="application/json")
        else:
            list_accounts = []
            for account_found in result:
                list_accounts.append(account_found.json_account())
            response = Response(json.dumps(list_accounts),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@account.route("/accounts/<account_id>", methods=["GET"])
@Auth.requires_token
def get_account_by_id(account_id):
    """This function searches for an account based on its ID."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({'id': account_id}):
        account_get = Account()
        account_get.id_member_ate = account_id
        result = account_get.consult_account()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_account()),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@account.route("/accounts/<account_id>", methods=["PUT"])
@Auth.requires_token
def change_account(account_id):
    """This function changes all the details of an account according to its ID."""
    json_values = request.json
    values_required = {"username", "name", "lastname", "dateBirth",
                       "email", "idCity"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idAccount"] = int(account_id)
        if validator_memberATE_change.is_valid(json_validator):
            account_change = Account()
            account_change.id_member_ate = int(account_id)
            account_change.username = json_values["username"]
            account_change.name = json_values["name"]
            account_change.lastname = json_values["lastname"]
            account_change.date_birth = json_values["dateBirth"]
            account_change.email = json_values["email"]
            account_change.id_city = json_values["idCity"]
            result = account_change.update_account()
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(json.dumps(account_change.json_account()),
                                    status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result,
                                    mimetype="application/json")
    return response


@account.route("/accounts/password/<account_id>", methods=["PATCH"])
@Auth.requires_token
def change_password(account_id):
    """This function changes the password of an account based on its ID."""
    json_values = request.json
    values_required = {"password", "newPassword"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idAccount"] = int(account_id)
        if validator_memberATE_password.is_valid(json_validator):
            account_change = Account()
            account_change.id_member_ate = int(account_id)
            account_change.password = encode_password(json_values["password"])
            result = account_change.update_password(encode_password(json_values["newPassword"]))
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(status=ResponsesREST.SUCCESSFUL.value)
            else:
                response = Response(json.dumps(json_error(result)), status=result,
                                    mimetype="application/json")
    return response
