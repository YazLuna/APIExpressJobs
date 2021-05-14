from flask import Blueprint
from src.model.serviceATE import ConnectServerService
from src.services.thrift.ttypes import ServiceRegistryUpdate

serviceATE = Blueprint("serviceATE", __name__)


@serviceATE.route("/services", methods=["POST"])
def add_service():
    pass


@serviceATE.route("/services", methods=["DELETE"])
def delete_member():
    pass


@serviceATE.route("/services", methods=["GET"])
def get_member():
    pass


@serviceATE.route("/services", methods=["GET"])
def get_members():
    pass


@serviceATE.route("/services", methods=["PUT"])
def update_member():
    pass
