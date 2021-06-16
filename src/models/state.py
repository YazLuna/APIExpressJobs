"""This module manages the states."""
from src.connect_database.connection_database import Connection
from src.routes.responses_rest import ResponsesREST


class State:
    """This class manages the states."""

    def __init__(self):
        self.id_state = ""
        self.id_country = ""
        self.name = ""
        self.connect = Connection.build_from_static()

    def get_state(self):
        """This function finds a status according to its ID."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCountry, name, idState FROM State WHERE idState = %s;"
        param = [self.id_state]
        states = self.connect.select(query, param)
        if states:
            state = State()
            state_found = states[0]
            state.name = state_found["name"]
            state.id_country = state_found["idCountry"]
            state.id_state = state_found["idState"]
            results = state
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def find_states(self):
        """This function finds the states of a country."""
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
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_state(self):
        """This function returns the state data in JSON serializable format."""
        return {"idState": self.id_state, "idCountry": self.id_country, "name": self.name}
