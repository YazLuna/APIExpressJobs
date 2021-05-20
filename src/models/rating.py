from src.connect_database.Connection import Connection


class Rating:
    def __init__(self):
        self.id_rating = ""
        self.comment = ""
        self.rating = ""
        self.id_request = ""
        self.connect = Connection.build_from_static()

    def add_rating(self):
        pass
