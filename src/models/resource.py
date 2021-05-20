from src.connect_database.Connection import Connection


class Resource:
    def __init__(self):
        self.id_resource = ""
        self.is_main_resource = ""
        self.route_save = ""
        self.name = ""
        self.id_service = ""
        self.connect = Connection.build_from_static()

    def add_resource(self):
        pass
