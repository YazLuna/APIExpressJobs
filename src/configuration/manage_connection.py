import json


class ManageConnection:
    @staticmethod
    def get_connection(key):
        information = None
        with open("src/configuration/connection.json") as json_file:
            data = json.load(json_file)
            if key in data:
                information = data[key]
        return information

    @staticmethod
    def set_data(key, new_data) -> bool:
        save_data = False
        with open("src/configuration/connection.json") as json_file:
            data_origin = json.load(json_file)
        open("src/configuration/connection.json", "w").close()
        data_origin[key] = new_data
        with open("src/configuration/connection.json", "w") as json_file:
            json.dump(data_origin, json_file, indent=2)
            save_data = True
        return save_data
