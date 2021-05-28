from src.connect_database.Connection import Connection
from src.models.account_role import AccountRole
from src.models.account_status import AccountStatus
from src.models.email import Email

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
        self.memberATE_status = AccountStatus.ACTIVE.value
        self.memberATE_type = AccountRole.CLIENT.value
        self.connect = Connection.build_from_static()

    def login(self):
        query = "SELECT memberATEType, idMemberATE FROM MemberATE WHERE username = %s AND password = %s"
        param = [self.username,
                 self.password]
        list_accounts = self.connect.select(query, param)
        account = False
        if list_accounts:
            account = Account()
            account_found = list_accounts[0]
            account.memberATE_type = account_found["memberATEType"]
            account.id_memberATE = account_found["idMemberATE"]
        return account

    def send_message(self, code):
        return Email.send_email(self.email, code)

    def add_memberATE(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.not_exist_account():
            query = "INSERT INTO MemberATE (email, dateBirth, lastName, name, idCity, idResource, username," \
                    " password, memberATEStatus, memberATEType) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
            param = [self.email,
                     self.date_birth,
                     self.lastName,
                     self.name,
                     self.id_city,
                     self.id_resource,
                     self.username,
                     self.password,
                     self.memberATE_status,
                     self.memberATE_type]
            result = self.connect.send_query(query, param)
            if result:
                self.id_memberATE = self.get_id()
                results = ResponsesREST.CREATED.value
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def get_id(self):
        query = "SELECT idMemberATE FROM MemberATE order by idMemberATE desc limit 1;"
        response = self.connect.select(query)
        account = Account()
        if response:
            id_list = response[0]
            account.id_memberATE = id_list["idMemberATE"]
        return account.id_memberATE

    def consult_account(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT email, dateBirth, lastName, name, idCity, idResource, username, password, memberATEType, " \
                "memberATEStatus FROM MemberATE WHERE idMemberATE = %s"
        param = [self.id_memberATE]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            account = Account()
            accounts_founds = list_accounts[0]
            account.email = accounts_founds["email"]
            account.name = accounts_founds["name"]
            account.lastName = accounts_founds["lastName"]
            account.date_birth = accounts_founds["dateBirth"]
            account.password = accounts_founds["password"]
            account.username = accounts_founds["username"]
            account.id_city = accounts_founds["idCity"]
            account.id_resource = accounts_founds["idResource"]
            account.memberATE_type = accounts_founds["memberATEType"]
            account.memberATE_status = accounts_founds["memberATEStatus"]
            results = account
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def consult_list_accounts(self, memberATEStatus, filter_search, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "email":
            query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus " \
                    "FROM MemberATE WHERE memberATEStatus = %s AND email = %s "
        else:
            if criterion == "name":
                query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus " \
                        "FROM MemberATE WHERE memberATEStatus = %s AND name = %s "
            else:
                if criterion == "lastname":
                    query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus " \
                            "FROM MemberATE WHERE memberATEStatus = %s AND lastName = %s "
        param = [memberATEStatus,
                 filter_search]
        if query is not None:
            list_account = self.connect.select(query, param)
            if list_account:
                account_list = []
                for accounts in list_account:
                    account = Account()
                    account.id_memberATE = accounts["idMemberATE"]
                    account.email = accounts["email"]
                    account.name = accounts["name"]
                    account.lastName = accounts["lastName"]
                    account.date_birth = accounts["dateBirth"]
                    account.memberATE_status = accounts["memberATEStatus"]
                    account.memberATE_type = accounts["memberATEType"]
                    account_list.append(account)
                results = account_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def update_account(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.not_exist_other_account():
            query = "UPDATE MemberATE SET email = %s, dateBirth = %s, lastName = %s, name = %s," \
                    " idCity = %s, username = %s, password = %s WHERE idMemberATE = %s; "
            param = [self.email,
                     self.date_birth,
                     self.lastName,
                     self.name,
                     self.id_city,
                     self.username,
                     self.password,
                     self.id_memberATE]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def change_status(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "UPDATE MemberATE SET memberATEStatus = %s WHERE idMemberATE = %s "
        param = [self.memberATE_status,
                 self.id_memberATE]
        result = self.connect.send_query(query, param)
        if result:
            results = ResponsesREST.SUCCESSFUL.value
        return results

    def add_employee_account(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "UPDATE MemberATE SET memberATEType = %s WHERE idMemberATE = %s "
        param = [self.memberATE_type,
                 self.id_memberATE]
        result = self.connect.send_query(query, param)
        if result:
            results = ResponsesREST.SUCCESSFUL.value
        return results

    def not_exist_other_account(self):
        result = True
        query = "SELECT idMemberATE FROM MemberATE WHERE idMemberATE <> %s AND ( email = %s OR username = %s)"
        param = [self.id_memberATE,
                 self.email,
                 self.username]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            result = False
        return result

    def not_exist_account(self):
        result = True
        query = "SELECT idMemberATE FROM MemberATE WHERE email = %s OR username = %s"
        param = [self.email,
                 self.username]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            result = False
        return result

    def json_account(self):
        return {"idMemberATE": self.id_memberATE, "username": self.username, "password": self.password,
                "name": self.name, "lastName": self.lastName, "dateBirth": self.date_birth,
                "email": self.email, "idCity": self.id_city, "idResource": self.id_resource,
                "memberATEType": self.memberATE_type, "memberATEStatus": self.memberATE_status}
