"""This module manages the requests."""
from src.connect_database.connection_database import Connection
from src.models.request_status import RequestStatus
from src.routes.responses_rest import ResponsesREST


class Request:
    """This class manages the requests."""

    def __init__(self):
        self.id_request = 0
        self.address = ""
        self.date = ""
        self.request_status = RequestStatus.REQUEST.value
        self.time = ""
        self.trouble = ""
        self.id_member_ate = 0
        self.id_service = 0
        self.connect = Connection.build_from_static()

    def add_request(self):
        """This function adds a request."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Request (address, date, requestStatus, " \
                "time, trouble, idMember, idService) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s); "
        param = [self.address,
                 self.date,
                 self.request_status,
                 self.time,
                 self.trouble,
                 self.id_member_ate,
                 self.id_service]
        result = self.connect.send_query(query, param)
        if result:
            self.id_request = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        """This function gets the ID of the created request."""
        query = "SELECT idRequest FROM Request order by idRequest desc limit 1;"
        response = self.connect.select(query)
        request = Request()
        if response:
            id_list = response[0]
            request.id_request = id_list["idRequest"]
        return request.id_request

    def get_request_by_id(self):
        """This function obtains the request information according to an ID."""
        request = ResponsesREST.SERVER_ERROR.value
        query = "SELECT address, date, requestStatus, time, trouble, idMember, idService " \
                "FROM Request WHERE idRequest = %s"
        param = [self.id_request]
        list_request = self.connect.select(query, param)
        if list_request:
            request = Request()
            list_request = list_request[0]
            request.id_request = int(self.id_request)
            request.address = list_request["address"]
            request.date = list_request["date"]
            request.date = request.date.strftime('%Y/%m/%d')
            request.request_status = list_request["requestStatus"]
            request.time = str(list_request["time"])
            request.trouble = list_request["trouble"]
            request.id_service = list_request["idService"]
            request.id_member_ate = list_request["idMember"]
        else:
            request = ResponsesREST.NOT_FOUND.value
        return request

    def find_request(self, request_status, filter_search, criterion):
        """This function obtains the request information according to a filter."""
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "memberATE":
            query = "SELECT S.name, R.address, R.date, R.requestStatus, R.time, R.trouble, " \
                    "R.idMember, R.idService, R.idRequest FROM Request R INNER JOIN MemberATE MA " \
                    "ON R.idMember = MA.idMemberATE INNER JOIN Service S on R.idService = " \
                    "S.idService WHERE R.requestStatus = %s AND" \
                    " MA.idMemberATE = %s;"
        else:
            if criterion == "service":
                query = "SELECT MA.name, MA.lastname, R.address, R.date, R.requestStatus, " \
                        "R.time, R.trouble, R.idMember, R.idService, R.idRequest FROM Request R " \
                        "INNER JOIN Service S ON R.idService = S.idService INNER JOIN MemberATE " \
                        "MA ON R.idMember = MA.idMemberATE WHERE R.requestStatus = %s " \
                        "AND S.idService = %s;"
        param = [request_status, filter_search]
        if query is not None:
            list_request = self.connect.select(query, param)
            if list_request:
                request_list = []
                if criterion == "memberATE":
                    for requests in list_request:
                        request = Request()
                        request.id_service = requests["name"]
                        request.id_request = requests["idRequest"]
                        request.id_member_ate = requests["idService"]
                        request.address = requests["address"]
                        request.request_status = requests["requestStatus"]
                        request.time = str(requests["time"])
                        request.date = requests["date"]
                        request.date = request.date.strftime('%Y/%m/%d')
                        request.trouble = requests["trouble"]
                        request_list.append(request)
                else:
                    for requests in list_request:
                        request = Request()
                        request.id_service = requests["idMember"]
                        request.id_request = requests["idRequest"]
                        request.id_member_ate = requests["name"] + " " + requests["lastname"]
                        request.address = requests["address"]
                        request.request_status = requests["requestStatus"]
                        request.time = str(requests["time"])
                        request.date = requests["date"]
                        request.date = request.date.strftime('%Y/%m/%d')
                        request.trouble = requests["trouble"]
                        request_list.append(request)
                results = request_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def find_request_service(self, service_id):
        """This function obtains the request information according to a filter."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT MA.name, MA.lastname, R.address, R.date, R.requestStatus, " \
                            "R.time, R.trouble, R.idMember, R.idService, R.idRequest FROM Request R " \
                            "INNER JOIN Service S ON R.idService = S.idService INNER JOIN MemberATE " \
                            "MA ON R.idMember = MA.idMemberATE WHERE S.idService = %s;"
        param = [service_id]
        if query is not None:
            list_request = self.connect.select(query, param)
            if list_request:
                request_list = []
                for requests in list_request:
                    request = Request()
                    request.id_service = requests["idService"]
                    request.id_request = requests["idRequest"]
                    request.id_member_ate = requests["name"] + " " + requests["lastname"]
                    request.address = requests["address"]
                    request.request_status = requests["requestStatus"]
                    request.time = str(requests["time"])
                    request.date = requests["date"]
                    request.date = request.date.strftime('%Y/%m/%d')
                    request.trouble = requests["trouble"]
                    request_list.append(request)
                results = request_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def change_status(self):
        """This function changes the status of a request."""
        results = ResponsesREST.SERVER_ERROR.value
        if self.request_exist():
            query = "UPDATE Request SET requestStatus = %s WHERE idRequest = %s "
            param = [self.request_status,
                     self.id_request]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def request_exist(self):
        """This function verifies that a request with that ID exists."""
        result = False
        query = "SELECT idRequest FROM Request WHERE idRequest = %s;"
        param = [self.id_request]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def json_request(self):
        """This function returns the request data in JSON serializable format."""
        return {"idRequest": self.id_request, "address": self.address,
                "date": self.date, "requestStatus": self.request_status,
                "time": self.time, "trouble": self.trouble,
                "idMemberATE": self.id_member_ate, "idService": self.id_service}
