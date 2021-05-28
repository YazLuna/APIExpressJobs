import json

from flask import Blueprint, Response

from src.models.account import Account
from src.models.account_role import AccountRole
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id

employee = Blueprint("Employees", __name__)


@employee.route("/employees/<idAccount>", methods=["PATCH"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def add_employee_account(idAccount):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": idAccount}):
        account_status = Account()
        account_status.id_memberATE = idAccount
        account_status.memberATE_type = AccountRole.CLIENT_EMPLOYEE.value
        result = account_status.add_employee_account()
        response = Response(status=result)
    return response
