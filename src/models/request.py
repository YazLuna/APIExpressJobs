from src.connect_database.Connection import Connection


class Request:
    def __init__(self):
        self.id_request = ""
        self.address = ""
        self.date = ""
        self.request_status = 1
        self.time = ""
        self.trouble = ""
        self.id_memberATE = ""
        self.id_service = ""
        self.connect = Connection.build_from_static()

    def add_request(self):
        pass
