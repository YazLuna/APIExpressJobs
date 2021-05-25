import json

from flask import Blueprint, request, Response

from src.models.state import State
from src.routes.auth import Auth
from src.routes.responses_rest import ResponsesREST

state = Blueprint("States", __name__)


@state.route("/states/<stateId>", methods=["GET"])
@Auth.requires_token
def get_state_by_id(stateId):
    state_get = State()
    state_get.id_state = stateId
    result = state_get.get_state()
    if result == ResponsesREST.INVALID_INPUT.value:
        response = Response(status=result)
    else:
        if result == ResponsesREST.SERVER_ERROR.value:
            response = Response(status=result)
        else:
            response = Response(json.dumps(result.json_state()), status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@state.route("/states", methods=["GET"])
@Auth.requires_token
def get_states():
    json_values = request.json
    values_required = {"idCountry"}
    response = Response(status=ResponsesREST.INVALID_INPUT.value)
    if all(key in json_values for key in values_required):
        # validator
        get_state = State()
        get_state.id_state = json_values["idCountry"]
        result = get_state.find_states()
        if result == ResponsesREST.INVALID_REQUEST.value:
            response = Response(status=result)
        else:
            if result == ResponsesREST.SERVER_ERROR.value:
                response = Response(status=result)
            else:
                list_states = []
                for states_found in result:
                    states_found.json_state()
                    list_states.append(states_found)
                response = Response(json.dumps(list_states), status=ResponsesREST.SUCCESSFUL.value,
                                    mimetype="application/json")
    return response
