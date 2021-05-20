from flask import Blueprint

message = Blueprint("Messages", __name__)


@message.route("/messages", methods=["POST"])
def add_message():
    pass


@message.route("/messages", methods=["GET"])
def find_messages(member_ate):  # noqa: E501
    pass


@message.route("/messages/{messageId}", methods=["GET"])
def get_message_by_id(message_id):  # noqa: E501
    pass
