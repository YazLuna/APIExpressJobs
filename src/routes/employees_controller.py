"""This module manages employee management."""
import json

from flask import Blueprint, Response

from src.models.account import Account
from src.models.account_role import AccountRole
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id

employee = Blueprint("Employees", __name__)


@employee.route("/employees/<id_account>", methods=["POST"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def add_employee_account(id_account):
    """This function adds the type of user employed to an already created account."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": id_account}):
        account_status = Account()
        account_status.id_memberATE = id_account
        account_status.memberATE_type = AccountRole.CLIENT_EMPLOYEE.value
        result = account_status.add_employee_account()
        if result == ResponsesREST.SUCCESSFUL.value:
            response = Response(status=result)
        else:
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
    return response
