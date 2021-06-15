"""This module manages the connection to the file server in C#."""
from thrift.transport.TTransport import TTransportException

from src.connect_file_server.connection import Communication
from src.routes.responses_rest import ResponsesREST
from src.services.thrift.ttypes import Resource


class ConnectServerResource(Communication):
    """This class manages the connection to the file server in C#."""

    def add_resource(self, resource: Resource):
        """This function opens and closes the connection to add an image."""
        try:
            self.communication_start()
            self.transport.open()
            resource = self.connection.AddResource(resource)
            self.transport.close()
        except TTransportException:
            resource = ResponsesREST.SERVER_ERROR.value
        return resource

    def delete_resource(self, route_save):
        """This function opens and closes the connection to delete an image."""
        try:
            self.communication_start()
            self.transport.open()
            response = self.connection.DeleteResource(route_save)
            self.transport.close()
        except TTransportException:
            response = ResponsesREST.SERVER_ERROR.value
        return response

    def consult_resource(self, route_save):
        """This function opens and closes the connection to consult an image."""
        try:
            self.communication_start()
            self.transport.open()
            resource = self.connection.GetResource(route_save)
            self.transport.close()
        except TTransportException:
            resource = ResponsesREST.SERVER_ERROR.value
        return resource

    def consult_resources_list(self, routes):
        """This function opens and closes the connection to consult a list of images."""
        try:
            self.communication_start()
            self.transport.open()
            resource = self.connection.GetResourcesList(routes)
            self.transport.close()
        except TTransportException:
            resource = ResponsesREST.SERVER_ERROR.value
        return resource
