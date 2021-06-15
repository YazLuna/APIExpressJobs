from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


class Rating:
    def __init__(self):
        self.id_rating = ""
        self.comment = ""
        self.rating = ""
        self.id_request = ""
        self.is_client = 0
        self.connect = Connection.build_from_static()

    def add_rating(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Rating (comment, rating, idRequest, isClient) VALUES ( %s, %s, %s, %s); "
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
        query = "SELECT idRating FROM Rating order by idRating desc limit 1;"
        response = self.connect.select(query)
        rating = Rating()
        if response:
            id_list = response[0]
            rating.id_rating = id_list["idRating"]
        return rating.id_rating

    def find_ratings(self, id, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "memberATE":
            query = "SELECT R.idRating, R.comment, R.rating, R.idRequest, S.name FROM Rating R " \
                    "INNER JOIN Request Rq ON R.idRequest = Rq.idRequest " \
                    "INNER JOIN Service S ON Rq.idService = S.idService " \
                    "WHERE Rq.idMember = %s AND isClient=1;"
        else:
            if criterion == "service":
                query = "SELECT R.idRating, R.comment, R.rating, R.idRequest, MA.name, MA.lastName FROM Rating R " \
                        "INNER JOIN Request Rq ON R.idRequest = Rq.idRequest " \
                        "INNER JOIN MemberATE MA ON Rq.idMember = MA.idMemberATE " \
                        "WHERE Rq.idService = %s AND isClient=2;"
        param = [id]
        if query is not None:
            list_ratings = self.connect.select(query, param)
            if list_ratings:
                rating_list = []
                if criterion == "memberATE":
                    for ratings in list_ratings:
                        rating = Rating()
                        rating.id_rating = ratings["idRating"]
                        rating.comment = ratings["comment"]
                        rating.rating = ratings["rating"]
                        rating.id_request = ratings["idRequest"]
                        rating.is_client = ratings["name"]
                        rating_list.append(rating)
                else:
                    for ratings in list_ratings:
                        rating = Rating()
                        rating.id_rating = ratings["idRating"]
                        rating.comment = ratings["comment"]
                        rating.rating = ratings["rating"]
                        rating.id_request = ratings["idRequest"]
                        rating.is_client = ratings["name"] + " " + ratings["lastName"]
                        rating_list.append(rating)
                results = rating_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def find_ratings_request(self):
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
        return {"idRating": self.id_rating, "comment": self.comment, "isClient": self.is_client,
                "rating": self.rating, "idRequest": self.id_request}
