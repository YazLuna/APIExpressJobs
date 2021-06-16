"""This module manages the connection to the configuration server REST methods."""
import requests
from requests import Response

from src.configuration.manage_connection import ManageConnection


class ConfigServer:
    """This class manages the connection to the configuration server REST methods."""

    def __init__(self, client_name: str):
        server_url = ManageConnection.get_connection("config_server_url")
        self.path = server_url + "/" + client_name

    def get(self, key: str, parameters: list = []) -> Response:
        """This function GET the configuration server."""
        return requests.get(self.path + "/" + key, params=parameters)

    def post(self, payload: dict or list = [], parameters: list = []) -> Response:
        """This function POST the configuration server."""
        return requests.post(self.path, json=payload, params=parameters)

    def put(self, payload: dict or list = [], parameters: list = []) -> Response:
        """This function PUT the configuration server."""
        return requests.put(self.path, json=payload, params=parameters)

    def patch(self, payload: dict or list = [], parameters: list = []) -> Response:
        """This function PATCH the configuration server."""
        return requests.patch(self.path, json=payload, params=parameters)

    def delete(self, payload: dict or list = [], parameters: list = []) -> Response:
        """This function DELETE the configuration server."""
        return requests.delete(self.path, json=payload, params=parameters)
