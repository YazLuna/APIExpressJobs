import json

from flask import Blueprint, request, Response

from src.models.account import Account
from src.models.account_role import AccountRole
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_memberATE, validator_change_status_member, validator_find_accounts, \
    validator_id

account = Blueprint("Accounts", __name__)


@account.route("/accounts", methods=["POST"])
def add_account():
    json_values = request.json
    values_required = {"username", "password", "name", "lastName", "dateBirth",
                       "email", "idCity"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_memberATE.is_valid(json_values):
            account_add = Account()
            account_add.username = json_values["username"]
            account_add.password = json_values["password"]
            account_add.name = json_values["name"]
            account_add.lastName = json_values["lastName"]
            account_add.date_birth = json_values["dateBirth"]
            account_add.email = json_values["email"]
            account_add.id_city = json_values["idCity"]
            account_add.id_resource = json_values["idResource"]
            result = account_add.add_memberATE()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(account_add.json_account()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@account.route("/accounts/<idAccount>", methods=["PATCH"])
@Auth.requires_token
def change_status_account(idAccount):
    json_values = request.json
    values_required = {"memberATEStatus"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idAccount"] = idAccount
        if validator_change_status_member.is_valid(json_validator):
            account_status = Account()
            account_status.id_memberATE = idAccount
            account_status.memberATE_status = json_values["memberATEStatus"]
            result = account_status.change_status()
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
            else:
                response = Response(status=result)
    return response


@account.route("/accounts/<memberATEStatus>/<filterSearch>/<criterion>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.MANAGER.name)
def find_accounts(memberATEStatus, filterSearch, criterion):
    json_validator = {"memberATEStatus": memberATEStatus, "filterSearch": filterSearch, "criterion": criterion}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_find_accounts.is_valid(json_validator):
        get_accounts = Account()
        result = get_accounts.consult_list_accounts(memberATEStatus, filterSearch, criterion)
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value \
                or result == ResponsesREST.INVALID_INPUT.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            list_accounts = []
            for account_found in result:
                list_accounts.append(account_found.json_account())
            response = Response(json.dumps(list_accounts), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@account.route("/accounts/<accountId>", methods=["GET"])
def get_account_by_id(accountId):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({'id': accountId}):
        account_get = Account()
        account_get.id_memberATE = accountId
        result = account_get.consult_account()
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_account()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@account.route("/accounts/<accountId>", methods=["PUT"])
@Auth.requires_token
def change_account(accountId):
    json_values = request.json
    values_required = {"username", "password", "name", "lastName", "dateBirth",
                       "email", "idCity"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        json_validator = json_values
        json_validator["idAccount"] = accountId
        if validator_memberATE.is_valid(json_validator):
            account_change = Account()
            account_change.id_memberATE = accountId
            account_change.username = json_values["username"]
            account_change.password = json_values["password"]
            account_change.name = json_values["name"]
            account_change.lastName = json_values["lastName"]
            account_change.date_birth = json_values["dateBirth"]
            account_change.email = json_values["email"]
            account_change.id_city = json_values["idCity"]
            result = account_change.update_account()
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(json.dumps(account_change.json_account()), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response
