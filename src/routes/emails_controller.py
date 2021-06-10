import json

from flask import Blueprint, request, Response

from src.models.account import Account, create_code
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_email

email = Blueprint("Emails", __name__)


@email.route("/emails", methods=["POST"])
def send_message_to_account():
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
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response
