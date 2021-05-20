import json

from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class AccountType:
    def __init__(self):
        self.id_account_type = ""
        self.account_status = ""
        self.account_type = ""
        self.id_account = ""
        self.connect = Connection.build_from_static()

    def add_account_type(self, id_account):
        results = ResponsesREST.SERVER_ERROR.value
        self.id_account = id_account
        query = "INSERT INTO AccountType (accountStatus, accountType, idAccount) " \
                "VALUES (%s, %s, %s); SELECT @@IDENTITY AS idAccountType "
        param = [self.account_status,
                 self.account_type,
                 self.id_account]
        result = self.connect.select(query, param)
        if result:
            self.id_account_type = result[0]["idAccountType"]
            results = ResponsesREST.CREATED.value
        return results

    def consult_account(self):
        pass

    def change_status(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.exist_account_type():
            query = "UPDATE AccountType SET accountStatus = %s " \
                    "WHERE idAccountType = %s "
            param = [self.account_status,
                     self.id_account_type]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def exist_account_type(self):
        query = "SELECT idAccountType FROM AccountType WHERE idAccountType = %s"
        param = [self.id_account_type]
        list_accounts = self.connect.select(query, param)
        result = False
        if list_accounts:
            result = True
        return result

    def json_account(self):
        json_converter = {"email": self.account_status, "account_status": self.account_type,
                          "id_account_type": self.id_account_type, "account": self.id_account}
        return json.dumps(json_converter)
