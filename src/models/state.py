from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class State:
    def __init__(self):
        self.id_state = ""
        self.id_country = ""
        self.name = ""
        self.connect = Connection.build_from_static()

    def get_state(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCountry, name, idState FROM State WHERE idState = %s;"
        param = [self.id_state]
        states = self.connect.select(query, param)
        if states:
            state = State()
            state.name = states["name"]
            state.id_country = states["idCountry"]
            state.id_state = states["idState"]
            results = state
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def find_states(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCountry, name, idState FROM State WHERE idCountry = %s;"
        param = [self.id_country]
        list_states = self.connect.select(query, param)
        if list_states:
            states_list = []
            for states in list_states:
                state = State()
                state.id_country = states["idCountry"]
                state.name = states["name"]
                state.id_state = states["idState"]
                states_list.append(state)
            results = states_list
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def json_state(self):
        return {"idState": self.id_state, "idCountry": self.id_country, "name": self.name}
