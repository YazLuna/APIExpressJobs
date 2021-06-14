"""This module manages the chats of the membersATE."""
from src.connect_database.connection_database import Connection
from src.routes.responses_rest import ResponsesREST


class Chat:
    """This class manages the chats of the membersATE."""

    def __init__(self):
        self.id_chat = 0
        self.id_service = 0
        self.id_member_ate = 0
        self.id_request = 0
        self.connect = Connection.build_from_static()

    def add_chat(self):
        """This function adds a chat."""
        results = ResponsesREST.SERVER_ERROR.value
        if self.request_exists():
            query = "INSERT INTO Chat (idService, idMemberATEClient, idRequest) " \
                    "VALUES (%s, %s, %s); "
            param = [self.id_service,
                     self.id_member_ate,
                     self.id_request]
            result = self.connect.send_query(query, param)
            if result:
                self.id_chat = self.get_id()
                results = ResponsesREST.CREATED.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def get_id(self):
        """This function gets the ID of the created chat."""
        query = "SELECT idChat FROM Chat order by idChat desc limit 1;"
        response = self.connect.select(query)
        chat = Chat()
        if response:
            id_list = response[0]
            chat.id_chat = id_list["idChat"]
        return chat.id_chat

    def request_exists(self):
        """This function verifies that there is a request, a service and a member
        with the entered ID."""
        result = False
        query = "SELECT idRequest FROM Request WHERE idRequest = %s AND idMember = %s " \
                "AND idService = %s;"
        param = [self.id_request,
                 self.id_member_ate,
                 self.id_service]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def find_chats(self, member_type):
        """This function obtains the chats according to a filter."""
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if member_type == "client":
            query = "SELECT C.idChat, C.idRequest, C.idMemberATEClient, S.idService FROM Chat C " \
                    "INNER JOIN Service S ON C.idService = S.idService INNER JOIN Request R" \
                    " ON C.idRequest = R.idRequest WHERE C.idMemberATEClient = %s " \
                    "AND (R.requestStatus = 1 OR R.requestStatus = 2);"
        else:
            if member_type == "employee":
                query = "SELECT C.idChat, C.idRequest, C.idMemberATEClient, S.idService " \
                        "FROM Chat C INNER JOIN Service S ON C.idService = S.idService " \
                        "INNER JOIN Request R ON C.idRequest = R.idRequest" \
                        " WHERE S.idMemberATE = %s " \
                        "AND (R.requestStatus = 1 OR R.requestStatus = 2);"
        param = [self.id_member_ate]
        if query is not None:
            list_chats = self.connect.select(query, param)
            if list_chats:
                chat_list = []
                for chats in list_chats:
                    chat = Chat()
                    chat.id_chat = chats["idChat"]
                    chat.id_request = chats["idRequest"]
                    chat.id_service = chats["idService"]
                    chat.id_member_ate = chats["idMemberATEClient"]
                    chat_list.append(chat)
                results = chat_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def json_chat(self):
        """This function returns the chat data in JSON serializable format."""
        return {"idChat": self.id_chat, "idRequest": self.id_request,
                "idService": self.id_service, "idMemberATE": self.id_member_ate}
