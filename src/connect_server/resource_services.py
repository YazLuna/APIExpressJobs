from src.connect_server.connection import Communication
from src.services.thrift.ttypes import Resource


class ConnectServerResource(Communication):

    def add_resource(self, resource: Resource):
        self.communication_start()
        self.transport.open()
        return self.connection.AddResource(resource)

    def delete_resource(self, resource: Resource):
        self.communication_start()
        self.transport.open()
        return self.connection.DeleteResource(resource)

    def consult_resource(self, resource: Resource):
        self.communication_start()
        self.transport.open()
        return self.connection.GetResource(resource)

    def consult_resources_list(self, idService):
        self.communication_start()
        self.transport.open()
        return self.connection.GetResourceList(idService)
