from datetime import date

from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


def getDate():
    today = date.today()
    return today.strftime("%Y/%m/%d")


class Message:
    def __init__(self):
        self.id_message = ""
        self.message = ""
        self.id_memberATE = ""
        self.id_service = ""
        self.id_request = ""
        self.date_time = getDate()
        self.memberType = ""
        self.connect = Connection.build_from_static()

    def add_message(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Message (message, idService, dateTime, memberType, idMemberATE) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s); "
        param = [self.message,
                 self.id_service,
                 self.date_time,
                 self.memberType,
                 self.id_memberATE]
        result = self.connect.send_query(query, param)
        if result:
            self.id_message = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idMessage FROM Message order by idMessage desc limit 1;"
        response = self.connect.select(query)
        message = Message()
        if response:
            id_list = response[0]
            message.id_message = id_list["idMessage"]
        return message.id_message

    def get_message(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT R.address, R.date, R.requestStatus, R.time, R.trouble, " \
                "R.idMember, R.idService, R.idRequest FROM Request R INNER JOIN " \
                "MemberATE MA ON R.idMember = MA.idMemberATE WHERE R.requestStatus = %s " \
                "AND MA.name = %s;"
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
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def get_messages_list(self):
        pass
