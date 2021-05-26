from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class City:
    def __init__(self):
        self.id_state = ""
        self.id_city = ""
        self.name = ""
        self.connect = Connection.build_from_static()

    def add_city(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO City (idCity, name, idState) VALUES (%s, %s, %s); "
        param = [self.id_city,
                 self.name,
                 self.id_state]
        result = self.connect.send_query(query, param)
        if result:
            self.id_city = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idCity FROM City order by idCity desc limit 1;"
        response = self.connect.select(query)
        city = City()
        if response:
            id_list = response[0]
            city.id_city = id_list["idCity"]
        return city.id_city

    def get_city(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCity, name, idState FROM City WHERE idCity = %s;"
        param = [self.id_city]
        cities = self.connect.select(query, param)
        if cities:
            city = City()
            city.name = cities["name"]
            city.id_city = cities["idCity"]
            city.id_state = cities["idState"]
            results = city
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def find_cities(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idCity, name, idState FROM City WHERE idState = %s;"
        param = [self.id_state]
        list_cities = self.connect.select(query, param)
        if list_cities:
            cities_list = []
            for cities in list_cities:
                city = City()
                city.id_city = cities["idCity"]
                city.name = cities["name"]
                city.id_state = cities["idState"]
                cities_list.append(city)
            results = cities_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_city(self):
        return {"idCity": self.id_city, "idState": self.id_state, "name": self.name}
