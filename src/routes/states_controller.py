"""This module manages the states."""
import json

from flask import Blueprint, Response

from src.models.state import State
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id

state = Blueprint("States", __name__)


@state.route("/states/<state_id>", methods=["GET"])
def get_state_by_id(state_id):
    """This function returns a status according to its ID."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": state_id}):
        state_get = State()
        state_get.id_state = state_id
        result = state_get.get_state()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_state()),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@state.route("/states/country/<id_country>", methods=["GET"])
def get_states(id_country):
    """This function returns all the states of a city."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": id_country}):
        get_state = State()
        get_state.id_country = id_country
        result = get_state.find_states()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_states = []
            for states_found in result:
                list_states.append(states_found.json_state())
            response = Response(json.dumps(list_states), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
