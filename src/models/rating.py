from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class Rating:
    def __init__(self):
        self.id_rating = ""
        self.comment = ""
        self.rating = ""
        self.id_request = ""
        self.connect = Connection.build_from_static()

    def add_rating(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Rating (comment, rating, idRequest) VALUES ( %s, %s, %s); "
        param = [self.comment,
                 self.rating,
                 self.id_request]
        result = self.connect.send_query(query, param)
        if result:
            self.id_rating = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idRating FROM Rating order by idRating desc limit 1;"
        response = self.connect.select(query)
        rating = Rating()
        if response:
            id_list = response[0]
            rating.id_rating = id_list["idRating"]
        return rating.id_rating

    def find_ratings(self, id_service):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT R.idRating, R.comment, R.rating, R.idRequest FROM Rating R " \
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
                rating_list.append(rating)
            results = rating_list
        else:
            results = ResponsesREST.INVALID_REQUEST.value
        return results

    def json_rating(self):
        return {"idRating": self.id_rating, "comment": self.comment,
                "rating": self.rating, "idRequest": self.id_request}
