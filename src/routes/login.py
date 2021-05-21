import json

from flask import Blueprint, request, Response, session

from src.models.account import Account
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

login = Blueprint("Logins", __name__)


@login.route("/logins", methods=["POST"])
def create_token():
    json_values = request.json
    values_required = {"username", "password"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        account_login = Account()
        account_login.username = json_values["username"]
        account_login.password = json_values["password"]
        result = account_login.login()
        if result:
            token = Auth.generate_token(account_login, 1)
            session.permanent = True
            session["token"] = token
            response = Response(json.dumps({"token": token}), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
        else:
            response = Response(status=result)
    return response
