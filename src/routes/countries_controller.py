"""This module manages the countries."""
import json

from flask import Blueprint, Response

from src.models.country import Country
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id

country = Blueprint("Countries", __name__)


@country.route("/countries/<country_id>", methods=["GET"])
def get_country_by_id(country_id):
    """This function gets a country according to its ID."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": country_id}):
        country_get = Country()
        country_get.id_country = country_id
        result = country_get.get_country()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_country()),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@country.route("/countries", methods=["GET"])
def get_countries():
    """This function retrieves all the countries in the database."""
    get_country = Country()
    result = get_country.find_countries()
    if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
        response = Response(json.dumps(json_error(result)),
                            status=result, mimetype="application/json")
    else:
        list_countries = []
        for countries_found in result:
            list_countries.append(countries_found.json_country())
        response = Response(json.dumps(list_countries),
                            status=ResponsesREST.SUCCESSFUL.value,
                            mimetype="application/json")
    return response
