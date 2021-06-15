"""This module manages the connection to the configuration server."""
import json


class ManageConnection:
    """This class manages the connection to the configuration server."""

    @staticmethod
    def get_connection(key):
        """This function obtains the connection to the configuration server."""
        information = None
        with open("src/configuration/connection.json") as json_file:
            data = json.load(json_file)
            if key in data:
                information = data[key]
        return information

    @staticmethod
    def set_data(key, new_data) -> bool:
        """This function connects to the configuration server."""
        save_data = False
        with open("src/configuration/connection.json") as json_file:
            data_origin = json.load(json_file)
        open("src/configuration/connection.json", "w").close()
        data_origin[key] = new_data
        with open("src/configuration/connection.json", "w") as json_file:
            json.dump(data_origin, json_file, indent=2)
            save_data = True
        return save_data
