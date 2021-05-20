from src.connect_database.Connection import Connection


class Service:
    def __init__(self):
        self.id_service = ""
        self.id_city = ""
        self.id_memberATE = ""
        self.name = ""
        self.description = ""
        self.slogan = ""
        self.type_service = ""
        self.working_hours = ""
        self.service_status = 1
        self.minimal_cost = ""
        self.maximum_cost = ""
        self.connect = Connection.build_from_static()

    def add_service(self):
        pass
