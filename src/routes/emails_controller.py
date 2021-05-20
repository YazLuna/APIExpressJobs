from flask import Blueprint

email = Blueprint("Emails", __name__)


@email.route("/emails", methods=["POST"])
def send_message_to_recover_account(email):
    pass
