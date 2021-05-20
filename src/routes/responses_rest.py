from enum import Enum


class ResponsesREST(Enum):
    CREATED = 201
    SUCCESSFUL = 200
    SERVER_ERROR = 500
    # For a input invalid
    INVALID_INPUT = 405
    # For a repeat object
    INVALID_REQUEST = 400
