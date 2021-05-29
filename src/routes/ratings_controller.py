import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.rating import Rating
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_rating, validator_id

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
            rating_add.comment = json_values["comment"]
            rating_add.rating = json_values["rating"]
            rating_add.id_request = json_values["idRequest"]
            result = rating_add.add_rating()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(rating_add.json_rating()), status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@rating.route("/ratings/<idService>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def find_ratings(idService):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": idService}):
        get_ratings = Rating()
        result = get_ratings.find_ratings(idService)
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            list_ratings = []
            for ratings_found in result:
                list_ratings.append(ratings_found.json_rating())
            response = Response(json.dumps(list_ratings), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
