import json

from src.connect_database.Connection import Connection
from src.models.account_type import AccountType

from src.routes.responses_rest import ResponsesREST


class Account:
    def __init__(self):
        self.id_memberATE = ""
        self.email = ""
        self.name = ""
        self.lastName = ""
        self.date_birth = ""
        self.username = ""
        self.password = ""
        self.id_city = ""
        self.id_resource = None
        self.id_account = ""
        self.connect = Connection.build_from_static()

    def add_memberATE(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.not_exist_account():
            query = "INSERT INTO MemberATE (email, dateBirth, lastName, name, idCity, idResource) " \
                    "VALUES (%s, %s, %s, %s, %s, %s); SELECT @@IDENTITY AS idMemberATE "
            param = [self.email,
                     self.date_birth,
                     self.lastName,
                     self.name,
                     self.id_city,
                     self.id_resource]
            result = self.connect.select(query, param)
            if result:
                self.id_memberATE = result[0]["idMemberATE"]
                results = self.add_account()
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def add_account(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Account (username, password, idMember) " \
                "VALUES (%s, %s, %s); SELECT @@IDENTITY AS idAccount "
        param = [self.username,
                 self.password,
                 self.id_memberATE]
        result = self.connect.select(query, param)
        if result:
            self.id_account = result[0]["idAccount"]
            results = AccountType.add_account_type(self.id_account)
        return results

    def consult_account(self):
        query = "SELECT * FROM MemberATE WHERE IdMemberATE = %s"
        param = [self.id_memberATE]
        list_accounts = self.connect.select(query, param)
        account = None
        if list_accounts:
            account = Account()
            list_accounts = list_accounts[0]
            account.email = list_accounts["email"]
            account.name = list_accounts["name"]
            account.lastName = list_accounts["lastName"]
            account.date_birth = list_accounts["dateBirth"]
        return account

    def consult_list_accounts(self):
        pass

    def update_account(self):
        pass

    def delete_account(self):
        pass

    def not_exist_account(self):
        result = True
        query = "SELECT M.idMemberATE FROM MemberATE M INNER JOIN Account A " \
                "ON M.idMemberATE = A.idMemberATE WHERE M.email = %s AND A.username = %s"
        param = [self.email,
                 self.username]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            result = False
        return result

    def json_account(self):
        json_converter = {"email": self.email, "name": self.name, "lastName": self.lastName,
                          "dateBirth": self.date_birth}
        return json.dumps(json_converter)
