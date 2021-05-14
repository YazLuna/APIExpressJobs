from src.model.connection import Communication
from src.services.thrift.ttypes import MemberATERegistryUpdate


class ConnectServerMember(Communication):
    def registry_member(self, member: MemberATERegistryUpdate):
        self.communication_start()
        self.transport.open()
        return self.connection.RegistryMemberATE(member)

    def delete_member(self, email):
        self.communication_start()
        self.transport.open()
        return self.connection.DeleteMemberATE(email)

    def consult_member(self, email):
        self.communication_start()
        self.transport.open()
        return self.connection.ConsultMemberATE(email)

    def consult_members(self):
        self.communication_start()
        self.transport.open()
        return self.connection.ConsultMembersATE()

    def update_member(self, member: MemberATERegistryUpdate):
        self.communication_start()
        self.transport.open()
        return self.connection.UpdateMemberATE(member)
