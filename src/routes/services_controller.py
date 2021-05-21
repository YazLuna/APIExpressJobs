import connexion
from flask import Blueprint

service = Blueprint("Services", __name__)


@service.route("/services", methods=["POST"])
def add_service(body, service=None):  # noqa: E501
    """Add a new service to the service catalog

    Add a new service # noqa: E501

    :param body: Service object that needs to be added to the catalog
    :type body: dict | bytes
    :param service: The service to create
    :type service: dict | bytes

    :rtype: None
    """
    return 'do some magic!'


@service.route("/services", methods=["PUT"])
def change_service(service=None):  # noqa: E501
    """Change data existing service

    Change the data of a service # noqa: E501

    :param service: The service to update
    :type service: dict | bytes

    :rtype: None
    """
    return 'do some magic!'


@service.route("/services", methods=["PATCH"])
def change_status(service_id, status):  # noqa: E501
    """Change status existing service

    Change the status of a service to block or unblock it # noqa: E501

    :param service_id: ID of service
    :type service_id: int
    :param status: status of service
    :type status: str

    :rtype: None
    """
    return 'do some magic!'


@service.route("/services", methods=["GET"])
def find_services(filter):  # noqa: E501
    """Return a list of Services

    Multiple filters values can be provided with comma separated strings # noqa: E501

    :param filter: Values that need to be considered for filter
    :type filter: List[str]

    :rtype: List[Service]
    """
    return 'do some magic!'


@service.route("/services/{serviceId}", methods=["GET"])
def get_service_by_id(service_id):  # noqa: E501
    """Returns a single service

    Find service by ID # noqa: E501

    :param service_id: ID of service to return
    :type service_id: int

    :rtype: Service
    """
    return 'do some magic!'