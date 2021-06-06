from src.connect_file_server.connection import Communication
from src.services.thrift.ttypes import Resource


class ConnectServerResource(Communication):

    def add_resource(self, resource: Resource):
        self.communication_start()
        self.transport.open()
        resource = self.connection.AddResource(resource)
        self.transport.close()
        return resource

    def delete_resource(self, route_save):
        self.communication_start()
        self.transport.open()
        response = self.connection.DeleteResource(route_save)
        self.transport.close()
        return response

    def consult_resource(self, route_save):
        self.communication_start()
        self.transport.open()
        resource = self.connection.GetResource(route_save)
        self.transport.close()
        return resource

    def consult_resources_list(self, routes):
        self.communication_start()
        self.transport.open()
        resource = self.connection.GetResourcesList(routes)
        self.transport.close()
        return resource
