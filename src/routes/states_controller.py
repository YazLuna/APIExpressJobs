import json

from flask import Blueprint, Response

from src.models.state import State
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id

state = Blueprint("States", __name__)


@state.route("/states/<stateId>", methods=["GET"])
def get_state_by_id(stateId):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": stateId}):
        state_get = State()
        state_get.id_state = stateId
        result = state_get.get_state()
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_state()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@state.route("/states/<idCountry>", methods=["GET"])
def get_states(idCountry):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": idCountry}):
        get_state = State()
        get_state.id_country = idCountry
        result = get_state.find_states()
        if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            list_states = []
            for states_found in result:
                list_states.append(states_found.json_state())
            response = Response(json.dumps(list_states), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
