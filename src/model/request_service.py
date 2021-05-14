from src.model.connection import Communication
from src.services.thrift.ttypes import RequestRegistry


class ConnectServerService(Communication):
    def registry_request(self, request: RequestRegistry):
        self.communication_start()
        self.transport.open()
        return self.connection.RegistryRequest(request)

    def update_request(self, status, id_report):
        self.communication_start()
        self.transport.open()
        return self.connection.UpdateStatusRequest(status, id_report)
