import json

from flask import Blueprint, request, Response

from src.models.state import State
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_id, validator_id_json

state = Blueprint("States", __name__)


@state.route("/states/<stateId>", methods=["GET"])
def get_state_by_id(stateId):
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": stateId}):
        state_get = State()
        state_get.id_state = stateId
        result = state_get.get_state()
        if result == ResponsesREST.NOT_FOUND.value:
            response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
        else:
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
            else:
                response = Response(json.dumps(result.json_state()), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
    return response


@state.route("/states", methods=["GET"])
def get_states():
    json_values = request.json
    values_required = {"idCountry"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_id_json.is_valid(json_values):
            get_state = State()
            get_state.id_state = json_values["idCountry"]
            result = get_state.find_states()
            if result == ResponsesREST.NOT_FOUND.value:
                response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
            else:
                if result == ResponsesREST.SERVER_ERROR.value:
                    response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
                else:
                    list_states = []
                    for states_found in result:
                        states_found.json_state()
                        list_states.append(states_found)
                    response = Response(json.dumps(list_states), status=ResponsesREST.SUCCESSFUL.value,
                                        mimetype="application/json")
    return response
