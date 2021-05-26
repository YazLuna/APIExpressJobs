import json

from flask import Blueprint, request, Response

from src.models.city import City
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST

city = Blueprint("Cites", __name__)


@city.route("/cities", methods=["POST"])
@Auth.requires_token
def add_city():
    json_values = request.json
    values_required = {"name", "idState"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        # validator
        city_add = City()
        city_add.name = json_values["name"]
        city_add.id_state = json_values["idState"]
        result = city_add.add_city()
        if result == ResponsesREST.CREATED.value:
            response = Response(json.dumps(city_add.json_city()), status=ResponsesREST.CREATED.value,
                                mimetype="application/json")
        else:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    return response


@city.route("/cities/<cityId>", methods=["GET"])
@Auth.requires_token
def get_city_by_id(cityId):
    city_get = City()
    city_get.id_city = cityId
    result = city_get.get_city()
    if result == ResponsesREST.NOT_FOUND.value:
        response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    else:
        if result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_city()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@city.route("/cities", methods=["GET"])
@Auth.requires_token
def get_cities():
    json_values = request.json
    values_required = {"idState"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        # validator
        get_city = City()
        get_city.id_state = json_values["idState"]
        result = get_city.find_cities()
        if result == ResponsesREST.NOT_FOUND.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
            else:
                list_cities = []
                for cities_found in result:
                    cities_found.json_city()
                    list_cities.append(cities_found)
                response = Response(json.dumps(list_cities), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
    return response
