from src.connect_database.Connection import Connection


class Report:
    def __init__(self):
        self.id_report = ""
        self.reason = ""
        self.id_service = ""
        self.id_memberATE = ""
        self.connect = Connection.build_from_static()

    def add_report(self):
        pass
