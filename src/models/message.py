"""This module manages the messages."""
from datetime import datetime

from src.connect_database.connection_database import Connection
from src.routes.responses_rest import ResponsesREST


def get_date():
    """This function gets the current date."""
    today = datetime.now()
    return today.strftime("%Y/%m/%d %H:%M:%S")


class Message:
    """This class manages the messages."""

    def __init__(self):
        self.id_message = 0
        self.message = ""
        self.date_time = get_date()
        self.member_type = 0
        self.id_chat = 0
        self.connect = Connection.build_from_static()

    def convert_date(self):
        """This function converts a date time to a string."""
        self.date_time = self.date_time.strftime("%Y/%m/%d %H:%M:%S")

    def add_message(self):
        """This function adds a message to the database."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Message (message, dateTime, memberType, idChat) " \
                "VALUES (%s, %s, %s, %s); "
        param = [self.message,
                 self.date_time,
                 self.member_type,
                 self.id_chat]
        result = self.connect.send_query(query, param)
        if result:
            self.id_message = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        """This function gets the ID of the created message."""
        query = "SELECT idMessage FROM Message order by idMessage desc limit 1;"
        response = self.connect.select(query)
        message = Message()
        if response:
            id_list = response[0]
            message.id_message = id_list["idMessage"]
        return message.id_message

    def get_messages_list(self):
        """This function gets the list of messages from a chat."""
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
                message.date_time = message.date_time.strftime("%Y/%m/%d %H:%M:%S")
                message.member_type = messages["memberType"]
                message_list.append(message)
            results = message_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_message(self):
        """This function returns the message data in JSON serializable format."""
        return {"idMessage": self.id_message, "message": self.message,
                "idChat": self.id_chat, "dateTime": self.date_time,
                "memberType": self.member_type}
