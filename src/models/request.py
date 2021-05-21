import json

from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class Request:
    def __init__(self):
        self.id_request = ""
        self.address = ""
        self.date = ""
        self.request_status = 1
        self.time = ""
        self.trouble = ""
        self.id_memberATE = ""
        self.id_service = ""
        self.connect = Connection.build_from_static()

    def add_request(self):
        results = ResponsesREST.SERVER_ERROR.value
        # Validar que exista el id
        query = "INSERT INTO Request (address, date, requestStatus, time, trouble, idMember, idService) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s); SELECT @@IDENTITY AS idRequest "
        param = [self.address,
                 self.date,
                 self.request_status,
                 self.time,
                 self.trouble,
                 self.id_memberATE,
                 self.id_service]
        result = self.connect.select(query, param)
        if result:
            self.id_request = result[0]["idRequest"]
            results = ResponsesREST.CREATED.value
        return results

    def get_request_by_id(self):
        query = "SELECT address, date, requestStatus, time, trouble, idMember, idService " \
                "FROM Request WHERE idRequest = %s"
        param = [self.id_request]
        list_request = self.connect.select(query, param)
        request = None
        if list_request:
            request = Request()
            list_request = list_request[0]
            request.address = list_request["address"]
            request.date = list_request["date"]
            request.request_status = list_request["requestStatus"]
            request.time = list_request["time"]
            request.trouble = list_request["trouble"]
            request.id_service = list_request["idService"]
            request.id_memberATE = list_request["idMember"]
        return request

    def find_request(self, filter):
        query = "SELECT address, date, requestStatus, time, trouble, idMember, idService, idRequest " \
                "FROM Request WHERE date = %s"
        param = [filter]
        list_request = self.connect.select(query, param)
        request_list = []
        if list_request:
            for requests in list_request:
                request = Request()
                request.id_request = requests["idRequest"]
                request.address = requests["address"]
                request.date = requests["date"]
                request.request_status = requests["requestStatus"]
                request.time = requests["time"]
                request.trouble = requests["trouble"]
                request.id_service = requests["idService"]
                request.id_memberATE = requests["idMember"]
                request_list.append(request)
        return request_list

    def change_status(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "UPDATE Request SET requestStatus = %s WHERE idRequest = %s "
        param = [self.request_status,
                 self.id_request]
        result = self.connect.send_query(query, param)
        if result:
            results = ResponsesREST.SUCCESSFUL.value
        return results

    def json_request(self):
        json_converter = {"address": self.address, "date": self.date, "request_status": self.request_status,
                          "time": self.time, "trouble": self.trouble}
        return json.dumps(json_converter)
