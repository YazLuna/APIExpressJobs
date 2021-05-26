import json
from datetime import datetime
from functools import update_wrapper

from cryptography.fernet import Fernet
from flask import session, Response, request

from src.models.account import Account
from src.routes.exception_responses_json import json_not_authorized, json_token_errors
from src.routes.responses_rest import ResponsesREST


class Auth:
    secret_password: bytes = None

    @staticmethod
    def set_password():
        Auth.secret_password = Fernet.generate_key()

    @staticmethod
    def requires_token(operation):
        def verify_auth(*args, **kwargs):
            token = request.headers.get("Token")
            saved_token = None
            try:
                saved_token = session["token"]
                if token is not None and saved_token is not None and token == saved_token:
                    session.modified = True
                    response = operation(*args, **kwargs)
                else:
                    response = Response(json.dumps(json_token_errors(ResponsesREST.NOT_AUTHENTICATED.value)),
                                        status=ResponsesREST.NOT_AUTHENTICATED.value,
                                        mimetype="application/json")
            except KeyError:
                if token is not None and saved_token is None:
                    response = Response(json.dumps(json_token_errors(ResponsesREST.TIME_OUT.value)),
                                        status=ResponsesREST.TIME_OUT.value,
                                        mimetype="application/json")
                else:
                    response = Response(json.dumps(json_token_errors(ResponsesREST.NOT_AUTHENTICATED.value)),
                                        status=ResponsesREST.NOT_AUTHENTICATED.value,
                                        mimetype="application/json")
            return response

        return update_wrapper(verify_auth, operation)

    @staticmethod
    def requires_role(role: str):
        def decorator(operation):
            def verify_role(*args, **kwargs):
                token = request.headers.get("Token")
                if token is not None:
                    values = Auth.decode_token(token)
                    if str(values["role"]) == str(role):
                        response = operation(*args, **kwargs)
                    else:
                        response = Response(json.dumps(json_not_authorized()), status=ResponsesREST.NOT_AUTHORIZED.value,
                                            mimetype="application/json")
                else:
                    response = Response(json.dumps(json_not_authorized()), status=ResponsesREST.NOT_AUTHORIZED.value,
                                        mimetype="application/json")
                return response

            return update_wrapper(verify_role, operation)

        return decorator

    @staticmethod
    def generate_token(account: Account) -> str:
        if Auth.secret_password is None:
            Auth.set_password()
        timestamp = datetime.now().strftime("%H:%M:%S")
        value: str = account.email + "/"
        value += account.password + "/"
        value += account.memberATE_type + "/"
        value += timestamp
        return Auth.encode(value, Auth.secret_password)

    @staticmethod
    def decode_token(token: str) -> dict:
        decoded_token = Auth.decode(token, Auth.secret_password)
        decoded_token = decoded_token.split("/")
        return {
            "email": decoded_token[0],
            "password": decoded_token[1],
            "role": decoded_token[2]
        }

    @staticmethod
    def encode(value: str, key: bytes) -> str:
        return Fernet(key).encrypt(value.encode()).decode()

    @staticmethod
    def decode(value: str, key: bytes) -> str:
        return Fernet(key).decrypt(value.encode()).decode()
