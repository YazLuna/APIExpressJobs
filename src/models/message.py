from src.connect_database.Connection import Connection


class Message:
    def __init__(self):
        self.id_message = ""
        self.message = ""
        self.id_memberATE = ""
        self.id_request = ""
        self.connect = Connection.build_from_static()

    def add_message(self):
        pass
