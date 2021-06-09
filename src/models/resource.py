from src.connect_database.Connection import Connection
from src.connect_file_server.resource_services import ConnectServerResource
from src.models.resource_type import ResourceType
from src.routes.responses_rest import ResponsesREST
from src.services.thrift.ttypes import Resource as ResourceStruct


class Resource:
    def __init__(self):
        self.id_resource = ""
        self.is_main_resource = ""
        self.route_save = ""
        self.name = ""
        self.id_service = 0
        self.id_memberATE = 0
        self.resource_file = None
        self.connect = Connection.build_from_static()

    def add_resource(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Resource (isMainResource, routeSave, name, idService, idMemberATE) " \
                "VALUES (%s, %s, %s, %s, %s); "
        param = [self.is_main_resource,
                 self.route_save,
                 self.name,
                 self.id_service,
                 self.id_memberATE]
        result = self.connect.send_query(query, param)
        if result:
            self.id_resource = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idResource FROM Resource order by idResource desc limit 1;"
        response = self.connect.select(query)
        resource = Resource()
        if response:
            id_list = response[0]
            resource.id_resource = id_list["idResource"]
        return resource.id_resource

    def add_resource_server(self):
        response = ResponsesREST.SERVER_ERROR.value
        self.route_save = self.get_route()
        connect = ConnectServerResource()
        resource_struct = ResourceStruct()
        resource_struct.name = self.name
        resource_struct.idService = self.id_service
        resource_struct.idMemberATE = self.id_memberATE
        resource_struct.isMainResource = self.is_main_resource
        resource_struct.routeSave = self.route_save
        resource_struct.resourceFile = self.resource_file.read()
        response = connect.add_resource(resource_struct)
        if response == ResponsesREST.CREATED.value:
            response = self.add_resource()
        return response

    def get_route(self):
        ext = self.resource_file.filename.split(".")[-1]
        route = "s" + str(self.id_service) + self.name + "." + ext
        if self.id_service == 0:
            route = "m" + str(self.id_memberATE) + self.name + "." + ext
            self.id_service = None
        else:
            self.id_memberATE = None
        return route

    def get_resource_server(self):
        response = ResponsesREST.SERVER_ERROR.value
        connect = ConnectServerResource()
        resource_struct = connect.consult_resource(self.route_save)
        if resource_struct.resourceFile is None:
            response = ResponsesREST.NOT_FOUND.value
        else:
            response = resource_struct
        return response

    def get_resource(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idResource, isMainResource, routeSave, name, idMemberATE, idService" \
                " FROM Resource WHERE idResource = %s"
        param = [self.id_resource]
        resource = self.connect.select(query, param)
        if resource:
            resource_found = resource[0]
            self.id_resource = resource_found["idResource"]
            self.is_main_resource = resource_found["isMainResource"]
            self.route_save = resource_found["routeSave"]
            self.name = resource_found["name"]
            self.id_memberATE = resource_found["idMemberATE"]
            self.id_service = resource_found["idService"]
            results = self
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def get_resource_list(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idResource, isMainResource, routeSave, name, idMemberATE, idService" \
                " FROM Resource WHERE idService = %s"
        param = [self.id_service]
        list_resource = self.connect.select(query, param)
        if list_resource:
            resource_list = []
            for resource_found in list_resource:
                resource = Resource()
                resource.id_resource = resource_found["idResource"]
                resource.is_main_resource = resource_found["isMainResource"]
                resource.route_save = resource_found["routeSave"]
                resource.name = resource_found["name"]
                resource.id_memberATE = resource_found["idMemberATE"]
                resource.id_service = resource_found["idService"]
                resource_list.append(resource)
            results = resource_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def get_main_resource(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idResource, isMainResource, routeSave, name, idMemberATE, idService" \
                " FROM Resource WHERE idService = %s AND isMainResource = %s;"
        self.is_main_resource = ResourceType.MAIN_RESOURCE.value
        param = [self.id_service, self.is_main_resource]
        list_resource = self.connect.select(query, param)
        if list_resource:
            resource_list = list_resource[0]
            resource = Resource()
            resource.id_resource = resource_list["idResource"]
            resource.is_main_resource = resource_list["isMainResource"]
            resource.route_save = resource_list["routeSave"]
            resource.name = resource_list["name"]
            resource.id_memberATE = resource_list["idMemberATE"]
            resource.id_service = resource_list["idService"]
            results = resource
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def delete_resource(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "DELETE FROM Resource WHERE routeSave = %s; "
        param = [self.route_save]
        result = self.connect.send_query(query, param)
        if result:
            results = ResponsesREST.SUCCESSFUL.value
        return results

    def delete_resource_server(self):
        response = ResponsesREST.SERVER_ERROR.value
        connect = ConnectServerResource()
        response = connect.delete_resource(self.route_save)
        if response == ResponsesREST.SUCCESSFUL.value:
            response = self.delete_resource()
        return response

    def json_resource(self):
        return {"idResource": self.id_resource, "isMainResource": self.is_main_resource,
                "name": self.name, "routeSave": self.route_save, "idService": self.id_service,
                "idMemberATE": self.id_memberATE}
