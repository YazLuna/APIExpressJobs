from flask import Blueprint, Response

from src.models.account import Account
from src.models.account_role import AccountRole
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

employee = Blueprint("Employees", __name__)


@employee.route("/employees/<idAccount>", methods=["PATCH"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def add_employee_account(idAccount):
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    account_status = Account()
    account_status.id_memberATE = idAccount
    account_status.memberATE_type = AccountRole.CLIENT_EMPLOYEE.value
    result = account_status.add_employee_account()
    response = Response(status=result)
    return response
