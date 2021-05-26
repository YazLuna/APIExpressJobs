from src.connect_database.Connection import Connection
from src.models.request_status import RequestStatus
from src.routes.responses_rest import ResponsesREST


class Request:
    def __init__(self):
        self.id_request = ""
        self.address = ""
        self.date = ""
        self.request_status = RequestStatus.REQUEST.value
        self.time = ""
        self.trouble = ""
        self.id_memberATE = ""
        self.id_service = ""
        self.connect = Connection.build_from_static()

    def add_request(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Request (address, date, requestStatus, time, trouble, idMember, idService) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s); "
        param = [self.address,
                 self.date,
                 self.request_status,
                 self.time,
                 self.trouble,
                 self.id_memberATE,
                 self.id_service]
        result = self.connect.send_query(query, param)
        if result:
            self.id_request = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idRequest FROM Request order by idRequest desc limit 1;"
        response = self.connect.select(query)
        request = Request()
        if response:
            id_list = response[0]
            request.id_request = id_list["idRequest"]
        return request.id_request

    def get_request_by_id(self):
        request = ResponsesREST.SERVER_ERROR.value
        query = "SELECT address, date, requestStatus, time, trouble, idMember, idService " \
                "FROM Request WHERE idRequest = %s"
        param = [self.id_request]
        list_request = self.connect.select(query, param)
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
        else:
            request = ResponsesREST.NOT_FOUND.value
        return request

    def find_request(self, request_status, filter_search, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        if criterion == "memberATE":
            query = "SELECT R.address, R.date, R.requestStatus, R.time, R.trouble, " \
                    "R.idMember, R.idService, R.idRequest FROM Request R INNER JOIN " \
                    "MemberATE MA ON R.idMember = MA.idMemberATE WHERE R.requestStatus = %s " \
                    "AND MA.name = %s;"
        else:
            query = "SELECT R.address, R.date, R.requestStatus, R.time, R.trouble, " \
                    "R.idMember, R.idService, R.idRequest FROM Request R INNER JOIN " \
                    "Service S on R.idService = S.idService WHERE R.requestStatus = %s " \
                    "AND S.name = %s;"
        param = [request_status,
                 filter_search]
        list_request = self.connect.select(query, param)
        if list_request:
            request_list = []
            for requests in list_request:
                request = Request()
                request.id_service = requests["idService"]
                request.name = requests["name"]
                request.description = requests["description"]
                request.slogan = requests["slogan"]
                request.type_service = requests["typeService"]
                request.working_hours = requests["workingHours"]
                request.service_status = requests["serviceStatus"]
                request.minimal_cost = requests["minimalCost"]
                request.maximum_cost = requests["maximumCost"]
                request_list.append(request)
            results = request_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

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
        return {"idRequest": self.id_request, "address": self.address,
                "date": self.date, "request_status": self.request_status,
                "time": self.time, "trouble": self.trouble,
                "idMemberATE": self.id_memberATE, "idService": self.id_service}
