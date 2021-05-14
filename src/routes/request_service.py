from flask import Blueprint

request_service = Blueprint("request_service", __name__)


@request_service.route("/requests", methods=["POST"])
def add_request():
    pass


@request_service.route("/requests", methods=["PUT"])
def update_request():
    pass
