from flask import Blueprint, request, Response
from src.model.memberATE import ConnectServerMember
from src.services.thrift.ttypes import MemberATERegistryUpdate

memberATE = Blueprint("memberATE", __name__)


@memberATE.route("/members", methods=["POST"])
def add_member():
    json_values = request.json
    new_member = MemberATERegistryUpdate(
        json_values["email"],
        json_values["name"],
        json_values["lastName"],
        json_values["dateBirth"]
    )
    add = ConnectServerMember()
    return Response(status=add.registry_member(new_member))


@memberATE.route("/members", methods=["DELETE"])
def delete_member():
    json_values = request.json
    email = json_values["email"]
    delete = ConnectServerMember()
    return Response(status=delete.delete_member(email))


@memberATE.route("/members", methods=["GET"])
def get_member():
    pass


@memberATE.route("/members", methods=["GET"])
def get_members():
    pass


@memberATE.route("/members", methods=["PUT"])
def update_member():
    pass
