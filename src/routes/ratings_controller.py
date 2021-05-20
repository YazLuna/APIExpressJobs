from flask import Blueprint

rating = Blueprint("Ratings", __name__)


@rating.route("/ratings", methods=["POST"])
def add_rating(body, rating=None):  # noqa: E501
    """Add a new rating to the service

    Add a new rating to the request of service # noqa: E501

    :param body: Rating object that needs to be added to the request
    :type body: dict | bytes
    :param rating: The rating to create
    :type rating: dict | bytes

    :rtype: None
    """
    return 'do some magic!'


@rating.route("/ratings", methods=["GET"])
def find_rating(id_service):  # noqa: E501
    """Return a list of rating

    Returns the average rating of a service # noqa: E501

    :param id_service: Service of which you want to know the rating
    :type id_service: int

    :rtype: InlineResponse2001
    """
    return 'do some magic!'
