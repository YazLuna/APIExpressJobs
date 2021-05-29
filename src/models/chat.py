from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class Chat:
    def __init__(self):
        self.id_chat = ""
        self.id_service = ""
        self.id_memberATE = ""
        self.id_request = ""
        self.connect = Connection.build_from_static()

    def add_chat(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Chat (idService, idMemberATEClient, idRequest) VALUES (%s, %s, %s); "
        param = [self.id_service,
                 self.id_memberATE,
                 self.id_request]
        result = self.connect.send_query(query, param)
        if result:
            self.id_chat = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idChat FROM Chat order by idChat desc limit 1;"
        response = self.connect.select(query)
        chat = Chat()
        if response:
            id_list = response[0]
            chat.id_chat = id_list["idChat"]
        return chat.id_chat

    def find_chats(self, memberType):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if memberType == "client":
            query = "SELECT C.idChat, C.idRequest, C.idMemberATEClient, S.idService FROM Chat C " \
                    "INNER JOIN Service S ON C.idService = S.idService INNER JOIN Request R" \
                    " ON C.idRequest = R.idRequest WHERE C.idMemberATEClient = %s " \
                    "AND (R.requestStatus = 1 OR R.requestStatus = 2);"
        else:
            if memberType == "employee":
                query = "SELECT C.idChat, C.idRequest, C.idMemberATEClient, S.idService FROM Chat C " \
                        "INNER JOIN Service S ON C.idService = S.idService INNER JOIN Request R" \
                        " ON C.idRequest = R.idRequest WHERE S.idMemberATE = %s " \
                        "AND (R.requestStatus = 1 OR R.requestStatus = 2);"
        param = [self.id_memberATE]
        if query is not None:
            list_chats = self.connect.select(query, param)
            if list_chats:
                chat_list = []
                for chats in list_chats:
                    chat = Chat()
                    chat.id_chat = chats["idChat"]
                    chat.id_request = chats["idRequest"]
                    chat.id_service = chats["idService"]
                    chat.id_memberATE = chats["idMemberATEClient"]
                    chat_list.append(chat)
                results = chat_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def json_chat(self):
        return {"idChat": self.id_chat, "idRequest": self.id_request,
                "idService": self.id_service, "idMemberATE": self.id_memberATE}
