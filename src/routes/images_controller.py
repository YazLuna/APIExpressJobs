import io
import json

from flask import Blueprint, Response, send_file

from src.models.resource import Resource
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST

image = Blueprint("Images", __name__)


@image.route("/images/<route>", methods=["GET"])
def get_image(route):
    resource_get = Resource()
    resource_get.route_save = route
    result = resource_get.get_resource_server()
    if result == ResponsesREST.NOT_FOUND.value or result == ResponsesREST.SERVER_ERROR.value:
        response = Response(json.dumps(json_error(result)), status=result, mimetype="application/json")
    else:
        response = send_file(io.BytesIO(result.resourceFile),
                             mimetype="image/png",
                             as_attachment=False)
    return response
