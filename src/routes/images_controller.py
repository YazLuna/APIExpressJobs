"""This module retrieves an image according to its path."""
import io
import json

from flask import Blueprint, Response, send_file

from src.models.resource import Resource
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST

image = Blueprint("Images", __name__)


@image.route("/images/<route>", methods=["GET"])
@Auth.requires_token
def get_image(route):
    """This function retrieves an image according to its path."""
    resource_get = Resource()
    resource_get.route_save = route
    result = resource_get.get_resource_server()
    if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
        response = Response(json.dumps(json_error(result)),
                            status=result, mimetype="application/json")
    else:
        response = send_file(io.BytesIO(result.resourceFile),
                             mimetype="image/png",
                             as_attachment=False)
    return response
