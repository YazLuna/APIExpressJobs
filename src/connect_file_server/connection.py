"""This module connects to the port where the C # server is running."""
from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport

from src.configuration.config_server import ConfigServer
from src.services.thrift.ResourcesServices import Client


class Communication:
    """This class connects to the port where the C # server is running."""

    def __init__(self):
        self.transport = ""
        self.connection = ""

    def communication_start(self):
        """This function starts communication."""
        config = ConfigServer("expressjobs")
        connect = config.patch(["hostServer", "portServer"]).json()
        host = connect["hostServer"]
        port = connect["portServer"]
        self.transport = TBufferedTransport(TSocket(host, port))
        protocol = TBinaryProtocol(self.transport)
        self.connection = Client(protocol)
