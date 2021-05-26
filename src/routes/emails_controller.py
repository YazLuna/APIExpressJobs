from flask import Blueprint, request, Response

from src.models.account import Account
from src.routes.responses_rest import ResponsesREST

email = Blueprint("Emails", __name__)


@email.route("/emails", methods=["POST"])
def send_message_to_account():
    json_values = request.json
    values = {"email", "messageSend"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values):
        # validator
        account = Account()
        account.email = json_values["email"]
        result = account.send_message(json_values["messageSend"])
        response = Response(status=result)
    return response
