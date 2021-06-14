"""This module manages the sending of messages to an email."""
import json

from flask import Blueprint, request, Response

from src.models.account import Account, create_code
from src.models.email import Email
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_email, validator_email_account

email = Blueprint("Emails", __name__)


@email.route("/emails", methods=["POST"])
def send_message_to_account():
    """This function updates the verification code and sends it to the email."""
    json_values = request.json
    values = {"email"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values):
        if validator_email.is_valid(json_values):
            account = Account()
            account.email = json_values["email"]
            result = account.change_code(create_code())
            if result == ResponsesREST.SUCCESSFUL.value:
                response = Response(json.dumps({"email": account.email}),
                                    status=result, mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@email.route("/emails/account", methods=["POST"])
def send_message_to_email():
    """This function sends a message to an email with the reason for its blocking, unblocking."""
    json_values = request.json
    values = {"email", "messageSend"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values):
        if validator_email_account.is_valid(json_values):
            result = Email.send_message_email(json_values["messageSend"], json_values["email"])
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps({"email": json_values["email"],
                                                "messageSend": json_values["messageSend"]}),
                                    status=result, mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result,
                                    mimetype="application/json")
    return response
