"""This module returns a JSON with the error information."""
from src.routes.responses_rest import ResponsesREST


def json_token_errors(code):
    """This function returns a JSON with information on errors 419 and 403."""
    result = {"error": "Requiere un token de acceso para poder usar esta funcionalidad"}
    if code == ResponsesREST.TIME_OUT.value:
        result = {"error": "Se agotado se tiempo en el sistema, por favor vuelva a iniciar sesión"}
    return result


def json_not_authorized():
    """This function returns a JSON with information on error 403."""
    return {"error": "No tiene permiso para realizar esta funcionalidad"}


def json_error(code_result):
    """This function returns a JSON with information on errors 400, 409, 500 and 404."""
    result = {"error": "Los datos que ingresó son inválidos, por favor ingrese datos correctos"}
    if code_result == ResponsesREST.SERVER_ERROR.value:
        result = {"error": "Problema de conexión, ingrese datos correctos o intente más tarde"}
    else:
        if code_result == ResponsesREST.INVALID_REQUEST:
            result = {"error": "Solicitud inválida, ya hay un objeto de este tipo registrado"}
        else:
            if code_result == ResponsesREST.NOT_FOUND.value:
                result = {"error": "No se encontró ningun objeto"}
    return result
