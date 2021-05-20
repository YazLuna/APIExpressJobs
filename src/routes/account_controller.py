from flask import Blueprint, request, Response

from src.models.account import Account
from src.models.account_type import AccountType
from src.routes.responses_rest import ResponsesREST

account = Blueprint("Accounts", __name__)


@account.route("/accounts", methods=["POST"])
def add_account():
    json_values = request.json
    values = {"username", "password", "name", "lastName", "dateBirth",
              "email", "id_city", "id_resource"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values):
        # validator
        account_add = Account()
        account_add.username = json_values["username"]
        account_add.password = json_values["password"]
        account_add.name = json_values["name"]
        account_add.lastName = json_values["lastName"]
        account_add.date_birth = json_values["dateBirth"]
        account_add.email = json_values["email"]
        account_add.id_city = json_values["id_city"]
        account_add.id_resource = json_values["id_resource"]
        result = account_add.add_memberATE()
        if result == ResponsesREST.CREATED.value:
            response = Response(account_add.json_account(), status=ResponsesREST.CREATED.value, mimetype="application/json")
        else:
            response = Response(status=result)
    return response


@account.route("/accounts", methods=["PATCH"])
def change_status_account():
    json_values = request.json
    values = {"id_account", "status"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values):
        # validator
        account_status = AccountType()
        account_status.id_account = json_values["id_account"]
        account_status.account_status = json_values["status"]
        result = account_status.change_status()
        if result == ResponsesREST.SUCCESSFUL.value:
            response = Response(account_status.json_account(), status=ResponsesREST.CREATED.value,
                                mimetype="application/json")
        else:
            response = Response(status=result)
    return response


@account.route("/accounts", methods=["GET"])
def find_accounts():
    pass


@account.route("/accounts/{accountId}", methods=["GET"])
def get_account_by_id():
    pass


@account.route("/accounts", methods=["PUT"])
def change_account():
    pass
