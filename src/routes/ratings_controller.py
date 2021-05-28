import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.rating import Rating
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id_json, validator_rating

rating = Blueprint("Ratings", __name__)


@rating.route("/ratings", methods=["POST"])
@Auth.requires_token
def add_rating():
    json_values = request.json
    values_required = {"comment", "rating", "idRequest"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_rating.is_valid(json_values):
            rating_add = Rating()
            rating_add.name = json_values["comment"]
            rating_add.description = json_values["rating"]
            rating_add.slogan = json_values["idRequest"]
            result = rating_add.add_rating()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(rating_add.json_rating()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@rating.route("/ratings", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def find_ratings():
    json_values = request.json
    values_required = {"idService"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_id_json.is_valid(json_values):
            get_ratings = Rating()
            result = get_ratings.find_ratings(json_values["idService"])
            if result == ResponsesREST.INVALID_REQUEST.value:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
            else:
                if result == ResponsesREST.SERVER_ERROR.value:
                    response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
                else:
                    list_ratings = []
                    for ratings_found in result:
                        ratings_found.json_rating()
                        list_ratings.append(ratings_found)
                    response = Response(json.dumps(list_ratings), status=ResponsesREST.SUCCESSFUL.value,
                                        mimetype="application/json")
    return response
