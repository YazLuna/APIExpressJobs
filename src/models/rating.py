"""This module manages the ratings."""
from src.connect_database.connection_database import Connection
from src.routes.responses_rest import ResponsesREST


class Rating:
    """This class manages the ratings."""

    def __init__(self):
        self.id_rating = ""
        self.comment = ""
        self.rating = ""
        self.id_request = ""
        self.is_client = 0
        self.connect = Connection.build_from_static()

    def add_rating(self):
        """This function adds a rating."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Rating (comment, rating, idRequest, isClient) " \
                "VALUES ( %s, %s, %s, %s); "
        param = [self.comment,
                 self.rating,
                 self.id_request,
                 self.is_client]
        result = self.connect.send_query(query, param)
        if result:
            self.id_rating = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        """This function gets the ID of the created request."""
        query = "SELECT idRating FROM Rating order by idRating desc limit 1;"
        response = self.connect.select(query)
        rating = Rating()
        if response:
            id_list = response[0]
            rating.id_rating = id_list["idRating"]
        return rating.id_rating

    def find_ratings(self, id_service):
        """This function gets the list of ratings from a service."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT R.idRating, R.comment, R.rating, R.idRequest, R.isClient FROM Rating R " \
                "INNER JOIN Request Rq ON R.idRequest = Rq.idRequest " \
                "WHERE Rq.idService = %s;"
        param = [id_service]
        list_ratings = self.connect.select(query, param)
        if list_ratings:
            rating_list = []
            for ratings in list_ratings:
                rating = Rating()
                rating.id_rating = ratings["idRating"]
                rating.comment = ratings["comment"]
                rating.rating = ratings["rating"]
                rating.id_request = ratings["idRequest"]
                rating.is_client = ratings["isClient"]
                rating_list.append(rating)
            results = rating_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def find_ratings_request(self):
        """This function gets the list of ratings from a request."""
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT R.idRating, R.comment, R.rating, R.idRequest, R.isClient FROM Rating R " \
                "WHERE R.idRequest = %s AND R.isClient= %s;"
        param = [self.id_request,
                 self.is_client]
        list_ratings = self.connect.select(query, param)
        if list_ratings:
            rating_list = []
            for ratings in list_ratings:
                rating = Rating()
                rating.id_rating = ratings["idRating"]
                rating.comment = ratings["comment"]
                rating.rating = ratings["rating"]
                rating.is_client = ratings["isClient"]
                rating.id_request = ratings["idRequest"]
                rating_list.append(rating)
            results = rating_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_rating(self):
        """This function returns the rating data in JSON serializable format."""
        return {"idRating": self.id_rating, "comment": self.comment, "isClient": self.is_client,
                "rating": self.rating, "idRequest": self.id_request}
