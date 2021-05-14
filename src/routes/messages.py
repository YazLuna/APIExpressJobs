from flask import Blueprint

message = Blueprint("message", __name__)


@message.route("/messages", methods=["GET"])
def get_messages():
    pass
