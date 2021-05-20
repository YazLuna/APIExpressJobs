from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport

from src.services.thrift.ResourcesServices import Client


class Communication:
    def communication_start(self):
        host = "localhost"
        port = 50000
        self.transport = TBufferedTransport(TSocket(host, port))
        protocol = TBinaryProtocol(self.transport)
        self.connection = Client(protocol)
