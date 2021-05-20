import requests
from requests import Response

from src.configuration.manage_connection import ManageConnection


class ConfigServer:
    def __init__(self, client_name: str):
        server_url = ManageConnection.get_connection("config_server_url")
        self.path = server_url + "/" + client_name

    def get(self, key: str, parameters: list = []) -> Response:
        return requests.get(self.path + "/" + key, params=parameters)

    def post(self, payload: dict or list = [], parameters: list = []) -> Response:
        return requests.post(self.path, json=payload, params=parameters)

    def put(self, payload: dict or list = [], parameters: list = []) -> Response:
        return requests.put(self.path, json=payload, params=parameters)

    def patch(self, payload: dict or list = [], parameters: list = []) -> Response:
        return requests.patch(self.path, json=payload, params=parameters)

    def delete(self, payload: dict or list = [], parameters: list = []) -> Response:
        return requests.delete(self.path, json=payload, params=parameters)
