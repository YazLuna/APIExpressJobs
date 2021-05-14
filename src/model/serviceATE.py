from src.model.connection import Communication
from src.services.thrift.ttypes import ServiceRegistryUpdate


class ConnectServerService(Communication):
    def registry_service(self, service: ServiceRegistryUpdate):
        self.communication_start()
        self.transport.open()
        return self.connection.RegistryServiceATE(service)

    def delete_service(self, id_service):
        self.communication_start()
        self.transport.open()
        return self.connection.DeleteServiceATE(id_service)

    def consult_service(self, id_service):
        self.communication_start()
        self.transport.open()
        return self.connection.ConsultServiceATE(id_service)

    def consult_services(self):
        self.communication_start()
        self.transport.open()
        return self.connection.ConsultMembersATE()

    def update_service(self, service: ServiceRegistryUpdate):
        self.communication_start()
        self.transport.open()
        return self.connection.UpdateServiceATE(service)
