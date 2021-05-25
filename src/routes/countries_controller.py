import json

from flask import Blueprint, Response

from src.models.country import Country
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

country = Blueprint("Countries", __name__)


@country.route("/countries/<countryId>", methods=["GET"])
@Auth.requires_token
def get_country_by_id(countryId):
    country_get = Country()
    country_get.id_state = countryId
    result = country_get.get_country()
    if result == ResponsesREST.INVALID_INPUT.value:
        response = Response(status=result)
    else:
        if result == ResponsesREST.SERVER_ERROR.value:
            response = Response(status=result)
        else:
            response = Response(json.dumps(result.json_country()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@country.route("/countries", methods=["GET"])
@Auth.requires_token
def get_countries():
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    get_country = Country()
    result = get_country.find_countries()
    if result == ResponsesREST.INVALID_REQUEST.value:
        response = Response(status=result)
    else:
        if result == ResponsesREST.SERVER_ERROR.value:
            response = Response(status=result)
        else:
            list_countries = []
            for countries_found in result:
                countries_found.json_country()
                list_countries.append(countries_found)
            response = Response(json.dumps(list_countries), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response