from thrift.transport.TTransport import TTransportException

from src.connect_file_server.connection import Communication
from src.routes.responses_rest import ResponsesREST
from src.services.thrift.ttypes import Resource


class ConnectServerResource(Communication):

    def add_resource(self, resource: Resource):
        try:
            self.communication_start()
            self.transport.open()
            resource = self.connection.AddResource(resource)
            self.transport.close()
        except TTransportException:
            resource = ResponsesREST.SERVER_ERROR.value
        return resource

    def delete_resource(self, route_save):
        try:
            self.communication_start()
            self.transport.open()
            response = self.connection.DeleteResource(route_save)
            self.transport.close()
        except TTransportException:
            response = ResponsesREST.SERVER_ERROR.value
        return response

    def consult_resource(self, route_save):
        try:
            self.communication_start()
            self.transport.open()
            resource = self.connection.GetResource(route_save)
            self.transport.close()
        except TTransportException:
            resource = ResponsesREST.SERVER_ERROR.value
        return resource

    def consult_resources_list(self, routes):
        try:
            self.communication_start()
            self.transport.open()
            resource = self.connection.GetResourcesList(routes)
            self.transport.close()
        except TTransportException:
            resource = ResponsesREST.SERVER_ERROR.value
        return resource
