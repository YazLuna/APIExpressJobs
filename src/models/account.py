import random

from src.connect_database.Connection import Connection
from src.models.account_role import AccountRole
from src.models.account_status import AccountStatus
from src.models.email import Email
from src.routes.responses_rest import ResponsesREST


def create_code():
    return random.randrange(1000000, 9999999)


class Account:
    def __init__(self):
        self.id_memberATE = 0
        self.email = ""
        self.name = ""
        self.lastName = ""
        self.date_birth = ""
        self.username = ""
        self.password = ""
        self.id_city = 0
        self.memberATE_status = AccountStatus.ACTIVE.value
        self.memberATE_type = AccountRole.CLIENT.value
        self.connect = Connection.build_from_static()

    def login(self):
        account = ResponsesREST.SERVER_ERROR.value
        if self.account_are_validated():
            query = "SELECT memberATEType, idMemberATE, idCity FROM MemberATE WHERE username = %s AND password = %s " \
                    "AND memberATEStatus = %s AND code IS NULL;"
            param = [self.username,
                     self.password,
                     self.memberATE_status]
            list_accounts = self.connect.select(query, param)
            account = ResponsesREST.NOT_FOUND.value
            if list_accounts:
                account = Account()
                account_found = list_accounts[0]
                account.memberATE_type = account_found["memberATEType"]
                account.id_memberATE = account_found["idMemberATE"]
                account.id_city = account_found["idCity"]
        else:
            account = ResponsesREST.INVALID_REQUEST.value
        return account

    def account_are_validated(self):
        response = True
        query = "SELECT idMemberATE FROM MemberATE WHERE username = %s AND password = %s " \
                "AND memberATEStatus = %s AND code IS NOT NULL;"
        param = [self.username,
                 self.password,
                 self.memberATE_status]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            response = False
        return response

    def validate_account(self, code):
        response = ResponsesREST.SERVER_ERROR.value
        if self.exist_account_to_validate(code):
            query = "UPDATE MemberATE SET code = %s WHERE password = %s AND username = %s"
            param = [None,
                     self.password,
                     self.username]
            list_accounts = self.connect.send_query(query, param)
            if list_accounts:
                response = ResponsesREST.SUCCESSFUL.value
        else:
            response = ResponsesREST.NOT_FOUND.value
        return response

    def exist_account_to_validate(self, code):
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE password = %s AND username = %s " \
                "AND code = %s"
        param = [self.password,
                 self.username,
                 code]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            result = True
        return result

    def send_message(self, code):
        return Email.send_email(self.email, code)

    def change_code(self, code):
        results = ResponsesREST.SERVER_ERROR.value
        if self.email_exists():
            query = "UPDATE MemberATE SET code = %s WHERE email = %s "
            param = [code,
                     self.email]
            result = self.connect.send_query(query, param)
            if result:
                self.send_message(code)
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def email_exists(self):
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE email = %s AND code IS NOT NULL;"
        param = [self.email]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def add_memberATE(self):
        results = ResponsesREST.SERVER_ERROR.value
        code = create_code()
        if self.not_exist_account():
            query = "INSERT INTO MemberATE (email, dateBirth, lastName, name, idCity, username, password, " \
                    "memberATEStatus, memberATEType, code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
            param = [self.email,
                     self.date_birth,
                     self.lastName,
                     self.name,
                     self.id_city,
                     self.username,
                     self.password,
                     self.memberATE_status,
                     self.memberATE_type,
                     code]
            result = self.connect.send_query(query, param)
            if result:
                self.id_memberATE = self.get_id()
                self.send_message(code)
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
        query = "SELECT idMemberATE, email, dateBirth, lastName, name, idCity, username, password, " \
                "memberATEType, memberATEStatus FROM MemberATE WHERE idMemberATE = %s"
        param = [self.id_memberATE]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            account = Account()
            accounts_founds = list_accounts[0]
            account.id_memberATE = accounts_founds["idMemberATE"]
            account.email = accounts_founds["email"]
            account.name = accounts_founds["name"]
            account.lastName = accounts_founds["lastName"]
            account.date_birth = accounts_founds["dateBirth"]
            account.date_birth = account.date_birth.strftime('%Y/%m/%d')
            account.password = accounts_founds["password"]
            account.username = accounts_founds["username"]
            account.id_city = accounts_founds["idCity"]
            account.memberATE_type = accounts_founds["memberATEType"]
            account.memberATE_status = accounts_founds["memberATEStatus"]
            results = account
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def consult_list_accounts(self, filter_search, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "email":
            query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus, idCity " \
                    "FROM MemberATE WHERE email = %s "
        else:
            if criterion == "name":
                query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus, " \
                        "idCity FROM MemberATE WHERE name = %s "
            else:
                if criterion == "lastname":
                    query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus, " \
                            "idCity FROM MemberATE WHERE lastName = %s "
                else:
                    if criterion == "status":
                        query = "SELECT idMemberATE, email, dateBirth, lastName, name, memberATEType, memberATEStatus, " \
                                "idCity FROM MemberATE WHERE memberATEStatus = %s "
        param = [filter_search]
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
                    account.date_birth = account.date_birth.strftime('%Y/%m/%d')
                    account.memberATE_status = accounts["memberATEStatus"]
                    account.memberATE_type = accounts["memberATEType"]
                    account.id_city = accounts["idCity"]
                    account_list.append(account)
                results = account_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def update_account(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_exists():
            if self.not_exist_other_account():
                query = "UPDATE MemberATE SET email = %s, dateBirth = %s, lastName = %s, name = %s," \
                        " idCity = %s, username = %s WHERE idMemberATE = %s; "
                param = [self.email,
                         self.date_birth,
                         self.lastName,
                         self.name,
                         self.id_city,
                         self.username,
                         self.id_memberATE]
                result = self.connect.send_query(query, param)
                if result:
                    results = ResponsesREST.SUCCESSFUL.value
            else:
                results = ResponsesREST.INVALID_REQUEST.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def update_password(self, new_password):
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_password_exists():
            query = "UPDATE MemberATE SET password = %s WHERE idMemberATE = %s AND password = %s; "
            param = [new_password,
                     self.id_memberATE,
                     self.password]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def change_status(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_exists():
            query = "UPDATE MemberATE SET memberATEStatus = %s WHERE idMemberATE = %s "
            param = [self.memberATE_status,
                     self.id_memberATE]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def add_employee_account(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_exists():
            query = "UPDATE MemberATE SET memberATEType = %s WHERE idMemberATE = %s "
            param = [self.memberATE_type,
                     self.id_memberATE]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def account_exists(self):
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE idMemberATE = %s;"
        param = [self.id_memberATE]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def account_password_exists(self):
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE idMemberATE = %s AND password = %s;"
        param = [self.id_memberATE,
                 self.password]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

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
                "email": self.email, "idCity": self.id_city, "memberATEType": self.memberATE_type,
                "memberATEStatus": self.memberATE_status}
