"""This module manages the accounts of membersATE."""
import random

from src.connect_database.connection_database import Connection
from src.models.account_role import AccountRole
from src.models.account_status import AccountStatus
from src.models.email import Email
from src.routes.responses_rest import ResponsesREST


def create_code():
    """This function creates the code to verify an account."""
    return random.randrange(1000000, 9999999)


class Account:
    """This class manages the accounts of membersATE."""

    def __init__(self):
        self.id_member_ate = 0
        self.email = ""
        self.name = ""
        self.lastname = ""
        self.date_birth = ""
        self.username = ""
        self.password = ""
        self.id_city = 0
        self.member_ate_status = AccountStatus.ACTIVE.value
        self.member_ate_type = AccountRole.CLIENT.value
        self.connect = Connection.build_from_static()

    def login(self):
        """This function logs in to the system."""
        account = ResponsesREST.SERVER_ERROR.value
        if self.account_are_validated():
            query = "SELECT memberATEType, idMemberATE, idCity FROM MemberATE " \
                    "WHERE username = %s AND password = %s " \
                    "AND memberATEStatus = %s AND code IS NULL;"
            param = [self.username,
                     self.password,
                     self.member_ate_status]
            list_accounts = self.connect.select(query, param)
            account = ResponsesREST.NOT_FOUND.value
            if list_accounts:
                account = Account()
                account_found = list_accounts[0]
                account.member_ate_type = account_found["memberATEType"]
                account.id_member_ate = account_found["idMemberATE"]
                account.id_city = account_found["idCity"]
        else:
            account = ResponsesREST.INVALID_REQUEST.value
        return account

    def account_are_validated(self):
        """This function checks if the account is already validated."""
        response = True
        query = "SELECT idMemberATE FROM MemberATE WHERE username = %s AND password = %s " \
                "AND memberATEStatus = %s AND code IS NOT NULL;"
        param = [self.username,
                 self.password,
                 self.member_ate_status]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            response = False
        return response

    def validate_account(self, code):
        """This function validates an account."""
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
        """This function checks if this account exists in order to validate it."""
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
        """This function sends the verification code to an account."""
        return Email.send_email(self.email, code)

    def change_code(self, code):
        """This function updates the verification code."""
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
        """This function checks if the email is not validated."""
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE email = %s AND code IS NOT NULL;"
        param = [self.email]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def add_member_ate(self):
        """This function adds an account in the database."""
        results = ResponsesREST.SERVER_ERROR.value
        code = create_code()
        if self.not_exist_account():
            query = "INSERT INTO MemberATE (email, dateBirth, lastname, name, idCity, " \
                    "username, password, memberATEStatus, memberATEType, code) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
            param = [self.email,
                     self.date_birth,
                     self.lastname,
                     self.name,
                     self.id_city,
                     self.username,
                     self.password,
                     self.member_ate_status,
                     self.member_ate_type,
                     code]
            result = self.connect.send_query(query, param)
            if result:
                self.id_member_ate = self.get_id()
                self.send_message(code)
                results = ResponsesREST.CREATED.value
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def get_id(self):
        """This function gets the ID of a created account."""
        query = "SELECT idMemberATE FROM MemberATE order by idMemberATE desc limit 1;"
        response = self.connect.select(query)
        account = Account()
        if response:
            id_list = response[0]
            account.id_member_ate = id_list["idMemberATE"]
        return account.id_member_ate

    def consult_account(self):
        """This function obtains the information of an account according to its ID."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idMemberATE, email, dateBirth, lastname, name, " \
                "idCity, username, password, memberATEType, memberATEStatus " \
                "FROM MemberATE WHERE idMemberATE = %s"
        param = [self.id_member_ate]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            account = Account()
            accounts_founds = list_accounts[0]
            account.id_member_ate = accounts_founds["idMemberATE"]
            account.email = accounts_founds["email"]
            account.name = accounts_founds["name"]
            account.lastname = accounts_founds["lastname"]
            account.date_birth = accounts_founds["dateBirth"]
            account.date_birth = account.date_birth.strftime('%Y/%m/%d')
            account.password = accounts_founds["password"]
            account.username = accounts_founds["username"]
            account.id_city = accounts_founds["idCity"]
            account.member_ate_type = accounts_founds["memberATEType"]
            account.member_ate_status = accounts_founds["memberATEStatus"]
            results = account
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def consult_list_accounts(self, filter_search, criterion):
        """This function obtains the account information according to a filter."""
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "email":
            query = "SELECT idMemberATE, email, dateBirth, username, lastname, " \
                    "name, memberATEType, memberATEStatus, " \
                    "idCity FROM MemberATE WHERE email = %s "
        else:
            if criterion == "name":
                query = "SELECT idMemberATE, email, dateBirth, username, lastname, name, " \
                        "memberATEType, memberATEStatus, idCity FROM MemberATE WHERE name = %s "
            else:
                if criterion == "lastname":
                    query = "SELECT idMemberATE, email, dateBirth, username, lastname, name, " \
                            "memberATEType, memberATEStatus, idCity FROM MemberATE " \
                            "WHERE lastname = %s "
                else:
                    if criterion == "status":
                        query = "SELECT idMemberATE, email, dateBirth, username, lastname, name, " \
                                "memberATEType, memberATEStatus, idCity FROM MemberATE " \
                                "WHERE memberATEStatus = %s "
        param = [filter_search]
        if query is not None:
            list_account = self.connect.select(query, param)
            if list_account:
                account_list = []
                for accounts in list_account:
                    account = Account()
                    account.id_member_ate = accounts["idMemberATE"]
                    account.email = accounts["email"]
                    account.name = accounts["name"]
                    account.username = accounts["username"]
                    account.lastname = accounts["lastname"]
                    account.date_birth = accounts["dateBirth"]
                    account.date_birth = account.date_birth.strftime('%Y/%m/%d')
                    account.member_ate_status = accounts["memberATEStatus"]
                    account.member_ate_type = accounts["memberATEType"]
                    account.id_city = accounts["idCity"]
                    account_list.append(account)
                results = account_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def update_account(self):
        """This function updates the details of an account."""
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_exists():
            if self.not_exist_other_account():
                query = "UPDATE MemberATE SET email = %s, dateBirth = %s, " \
                        "lastname = %s, name = %s, idCity = %s, username = %s " \
                        "WHERE idMemberATE = %s; "
                param = [self.email,
                         self.date_birth,
                         self.lastname,
                         self.name,
                         self.id_city,
                         self.username,
                         self.id_member_ate]
                result = self.connect.send_query(query, param)
                if result:
                    results = ResponsesREST.SUCCESSFUL.value
            else:
                results = ResponsesREST.INVALID_REQUEST.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def update_password(self, new_password):
        """This function updates the password for an account."""
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_password_exists():
            query = "UPDATE MemberATE SET password = %s WHERE idMemberATE = %s AND password = %s; "
            param = [new_password,
                     self.id_member_ate,
                     self.password]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def change_status(self):
        """This function changes the status of an account."""
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_exists():
            query = "UPDATE MemberATE SET memberATEStatus = %s WHERE idMemberATE = %s "
            param = [self.member_ate_status,
                     self.id_member_ate]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def add_employee_account(self):
        """This function updates an account so that it can be employed."""
        results = ResponsesREST.SERVER_ERROR.value
        if self.account_exists():
            query = "UPDATE MemberATE SET memberATEType = %s WHERE idMemberATE = %s "
            param = [self.member_ate_type,
                     self.id_member_ate]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def account_exists(self):
        """This function verifies that the account ID exists."""
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE idMemberATE = %s;"
        param = [self.id_member_ate]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def account_password_exists(self):
        """This function verifies that there is an account with that ID and password."""
        result = False
        query = "SELECT idMemberATE FROM MemberATE WHERE idMemberATE = %s AND password = %s;"
        param = [self.id_member_ate,
                 self.password]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def not_exist_other_account(self):
        """This function verifies that there is no other account with that email or password."""
        result = True
        query = "SELECT idMemberATE FROM MemberATE WHERE idMemberATE <> %s " \
                "AND ( email = %s OR username = %s)"
        param = [self.id_member_ate,
                 self.email,
                 self.username]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            result = False
        return result

    def not_exist_account(self):
        """This function verifies that there is no account with that email or password."""
        result = True
        query = "SELECT idMemberATE FROM MemberATE WHERE email = %s OR username = %s"
        param = [self.email,
                 self.username]
        list_accounts = self.connect.select(query, param)
        if list_accounts:
            result = False
        return result

    def json_account(self):
        """This function returns the account data in JSON serializable format."""
        return {"idAccount": self.id_member_ate, "username": self.username,
                "password": self.password, "name": self.name,
                "lastname": self.lastname, "dateBirth": self.date_birth,
                "email": self.email, "idCity": self.id_city, "memberATEType": self.member_ate_type,
                "memberATEStatus": self.member_ate_status}
