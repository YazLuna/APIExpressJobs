from src.model.connection import Communication
from src.services.thrift.ttypes import Message


class ConnectServerService(Communication):
    def get_messages(self):
        self.communication_start()
        self.transport.open()
        return self.connection.GetMessagesChat()
