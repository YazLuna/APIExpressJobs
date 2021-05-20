from flask import Blueprint

resource = Blueprint("Resources", __name__)


@resource.route("/resources", methods=["POST"])
def add_resource(body, resource=None):  # noqa: E501
    """Adds a multimedia resource item

    Add a multimedia resource to the system, if it already exists, overwrite it # noqa: E501

    :param body: Resource object that needs to be added to the catalog
    :type body: dict | bytes
    :param resource: The resource to create
    :type resource: dict | bytes

    :rtype: None
    """
    return 'do some magic!'


@resource.route("/resources", methods=["DELETE"])
def delete_resource(resource_id):  # noqa: E501
    """Remove the resource

    Remove the resource from a specific service # noqa: E501

    :param resource_id: ID of resource
    :type resource_id: int

    :rtype: None
    """
    return 'do some magic!'


@resource.route("/resources", methods=["GET"])
def find_resources(id_service):  # noqa: E501
    """Returns a list of Resources

    Returns a list of resources from a specific service # noqa: E501

    :param id_service: Associated service identifier
    :type id_service: int

    :rtype: List[Resource]
    """
    return 'do some magic!'


@resource.route("/resources/{resourceId}", methods=["GET"])
def get_resource_by_id(resource_id):  # noqa: E501
    """Returns a single resource

    Find resource by ID # noqa: E501

    :param resource_id: ID of resource to return
    :type resource_id: int

    :rtype: Resource
    """
    return 'do some magic!'
