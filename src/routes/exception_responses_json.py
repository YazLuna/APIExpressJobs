from src.routes.responses_rest import ResponsesREST


def json_token_errors(code):
    result = {"error": "Requiere un token de acceso para poder usar esta funcionalidad"}
    if code == ResponsesREST.TIME_OUT.value:
        result = {"error": "Se agotado se tiempo en el sistema, por favor vuelva a iniciar sesión"}
    return result


def json_not_authorized():
    return {"error": "No tiene permiso para realizar esta funcionalidad"}


def json_error(code_result):
    result = {"error": "Los datos que ingresó son inválidos, por favor ingrese datos correctos"}
    if code_result == ResponsesREST.SERVER_ERROR.value:
        result = {"error": "Problema de conexión con la base de datos, ingrese datos correctos"}
    else:
        if code_result == ResponsesREST.INVALID_REQUEST:
            result = {"error": "Solicitud inválida, ya hay un objeto de este tipo registrado"}
        else:
            if code_result == ResponsesREST.NOT_FOUND.value:
                result = {"error": "No se encontró ningun objeto"}
    return result
