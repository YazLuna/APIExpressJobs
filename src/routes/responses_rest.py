from enum import Enum


class ResponsesREST(Enum):
    CREATED = 201
    SUCCESSFUL = 200
    SERVER_ERROR = 500
    INVALID_INPUT = 400
    # For a repeat object
    INVALID_REQUEST = 409
    NOT_AUTHORIZED = 403
    NOT_AUTHENTICATED = 401
    TIME_OUT = 419
    NOT_FOUND = 404
