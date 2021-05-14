from src.model.connection import Communication
from src.services.thrift.ttypes import Report


class ConnectServerService(Communication):
    def registry_report(self, report: Report):
        self.communication_start()
        self.transport.open()
        return self.connection.RegistryReport(report)

