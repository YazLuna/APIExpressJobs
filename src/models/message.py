from datetime import datetime

from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


def getDate():
    today = datetime.now()
    return today.strftime("%Y/%m/%d %H:%M:%S")


class Message:
    def __init__(self):
        self.id_message = 0
        self.message = ""
        self.date_time = getDate()
        self.memberType = 0
        self.id_chat = 0
        self.connect = Connection.build_from_static()

    def convert_date(self):
        self.date_time = self.date_time.strftime("%Y/%m/%d %H:%M:%S")

    def add_message(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Message (message, dateTime, memberType, idChat) " \
                "VALUES (%s, %s, %s, %s); "
        param = [self.message,
                 self.date_time,
                 self.memberType,
                 self.id_chat]
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

    def get_messages_list(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idMessage, message, idChat, dateTime, memberType FROM Message " \
                "WHERE idChat = %s;"
        param = [self.id_chat]
        list_messages = self.connect.select(query, param)
        if list_messages:
            message_list = []
            for messages in list_messages:
                message = Message()
                message.id_message = messages["idMessage"]
                message.message = messages["message"]
                message.id_chat = messages["idChat"]
                message.date_time = messages["dateTime"]
                message.date_time = message.date_time.strftime('%Y/%m/%d')
                message.memberType = messages["memberType"]
                message_list.append(message)
            results = message_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_message(self):
        return {"idMessage": self.id_message, "message": self.message,
                "idChat": self.id_chat, "dateTime": self.date_time,
                "memberType": self.memberType}
