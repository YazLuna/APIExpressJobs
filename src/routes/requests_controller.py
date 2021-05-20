from flask import Blueprint

request = Blueprint("Requests", __name__)


@request.route("/requests", methods=["POST"])
def add_request(body, request=None):  # noqa: E501
    """Add a new request to the Catalogue

    Add a new request # noqa: E501

    :param body: Request object that needs to be added to the request
    :type body: dict | bytes
    :param request: The request to create
    :type request: dict | bytes

    :rtype: None
    """
    return 'do some magic!'


@request.route("/requests", methods=["PATCH"])
def change_status_request(request_id, status):  # noqa: E501
    """Change status existing request

    Change the status of a service to cancelled, rejected or accept # noqa: E501

    :param request_id: ID of request
    :type request_id: int
    :param status: status of request
    :type status: str

    :rtype: None
    """
    return 'do some magic!'


@request.route("/requests", methods=["GET"])
def find_requests(filter):  # noqa: E501
    """Finds Requests

    Multiple filters values can be provided with comma separated strings # noqa: E501

    :param filter: Values that need to be considered for filter
    :type filter: List[str]

    :rtype: List[Request]
    """
    return 'do some magic!'


@request.route("/requests/{requestId}", methods=["POST"])
def get_request_by_id(request_id):  # noqa: E501
    """Find request by ID

    Returns a single request # noqa: E501

    :param request_id: ID of request to return
    :type request_id: int

    :rtype: Request
    """
    return 'do some magic!'
