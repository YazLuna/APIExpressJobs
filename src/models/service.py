from src.connect_database.Connection import Connection
from src.models.services_status import ServiceStatus
from src.routes.responses_rest import ResponsesREST


class Service:
    def __init__(self):
        self.id_service = 0
        self.id_city = 0
        self.id_memberATE = 0
        self.name = ""
        self.description = ""
        self.slogan = ""
        self.type_service = ""
        self.working_hours = ""
        self.service_status = ServiceStatus.ACTIVE.value
        self.minimal_cost = 0
        self.maximum_cost = 0
        self.connect = Connection.build_from_static()

    def add_service(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Service (idCity, idMemberATE, name, description, slogan, typeService, workingHours," \
                " serviceStatus, minimalCost, maximumCost) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s); "
        param = [self.id_city,
                 self.id_memberATE,
                 self.name,
                 self.description,
                 self.slogan,
                 self.type_service,
                 self.working_hours,
                 self.service_status,
                 self.minimal_cost,
                 self.maximum_cost]
        result = self.connect.send_query(query, param)
        if result:
            self.id_service = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idService FROM Service order by idService desc limit 1;"
        response = self.connect.select(query)
        service = Service()
        if response:
            id_list = response[0]
            service.id_service = id_list["idService"]
        return service.id_service

    def change_status(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.service_exist():
            query = "UPDATE Service SET serviceStatus = %s WHERE idService = %s "
            param = [self.service_status,
                     self.id_service]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def consult_service(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idService, idCity, idMemberATE, name, description, slogan, typeService, workingHours, " \
                "serviceStatus, minimalCost, maximumCost FROM Service WHERE idService = %s"
        param = [self.id_service]
        list_services = self.connect.select(query, param)
        if list_services:
            service = Service()
            services_founds = list_services[0]
            service.id_service = services_founds["idService"]
            service.id_city = services_founds["idCity"]
            service.id_memberATE = services_founds["idMemberATE"]
            service.name = services_founds["name"]
            service.description = services_founds["description"]
            service.slogan = services_founds["slogan"]
            service.type_service = services_founds["typeService"]
            service.working_hours = services_founds["workingHours"]
            service.service_status = services_founds["serviceStatus"]
            service.minimal_cost = services_founds["minimalCost"]
            service.maximum_cost = services_founds["maximumCost"]
            results = service
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def change_service(self):
        results = ResponsesREST.SERVER_ERROR.value
        if self.service_member_exist():
            query = "UPDATE Service SET idCity = %s, name = %s, description = %s," \
                    " slogan = %s, typeService = %s, workingHours = %s," \
                    " minimalCost = %s, maximumCost = %s " \
                    "WHERE idService = %s AND idMemberATE = %s; "
            param = [self.id_city,
                     self.name,
                     self.description,
                     self.slogan,
                     self.type_service,
                     self.working_hours,
                     self.minimal_cost,
                     self.maximum_cost,
                     self.id_service,
                     self.id_memberATE]
            result = self.connect.send_query(query, param)
            if result:
                results = ResponsesREST.SUCCESSFUL.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def service_exist(self):
        result = False
        query = "SELECT idService FROM Service WHERE idService = %s;"
        param = [self.id_service]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def service_member_exist(self):
        result = False
        query = "SELECT idService FROM Service WHERE idService = %s AND idMemberATE = %s;"
        param = [self.id_service,
                 self.id_memberATE]
        response = self.connect.select(query, param)
        if response:
            result = True
        return result

    def consult_list_services(self, serviceStatus, filter_search, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "typeService":
            query = "SELECT idService, name, description, slogan, typeService, workingHours, serviceStatus" \
                    ", minimalCost, maximumCost, idCity, idMemberATE FROM Service WHERE serviceStatus = %s " \
                    "AND typeService = %s "
        else:
            if criterion == "name":
                query = "SELECT idService, name, description, slogan, typeService, workingHours, serviceStatus" \
                        ", minimalCost, maximumCost, idCity, idMemberATE FROM Service WHERE serviceStatus = %s " \
                        "AND name = %s "
            else:
                if criterion == "minimalCost":
                    query = "SELECT idService, name, description, slogan, typeService, workingHours, serviceStatus" \
                            ", minimalCost, maximumCost, idCity, idMemberATE FROM Service WHERE serviceStatus = %s " \
                            "AND minimalCost = %s "
                else:
                    if criterion == "maximumCost":
                        query = "SELECT idService, name, description, slogan, typeService, workingHours, serviceStatus" \
                                ", minimalCost, maximumCost, idCity, idMemberATE FROM Service WHERE serviceStatus = %s " \
                                "AND maximumCost = %s "
        param = [serviceStatus, filter_search]
        if query is not None:
            list_services = self.connect.select(query, param)
            if list_services:
                services_list = []
                for services in list_services:
                    service = Service()
                    service.id_service = services["idService"]
                    service.name = services["name"]
                    service.description = services["description"]
                    service.slogan = services["slogan"]
                    service.type_service = services["typeService"]
                    service.working_hours = services["workingHours"]
                    service.service_status = services["serviceStatus"]
                    service.minimal_cost = services["minimalCost"]
                    service.maximum_cost = services["maximumCost"]
                    service.id_city = services["idCity"]
                    service.id_memberATE = services["idMemberATE"]
                    services_list.append(service)
                results = services_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def consult_list_services_city(self, filter_search, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "typeService":
            query = "SELECT idService, name, description, slogan, typeService, workingHours" \
                    ", minimalCost, maximumCost, idMemberATE, idCity FROM Service WHERE serviceStatus = %s " \
                    "AND typeService = %s AND idCity = %s;"
        else:
            if criterion == "name":
                query = "SELECT idService, name, description, slogan, typeService, workingHours" \
                        ", minimalCost, maximumCost, idMemberATE, idCity FROM Service WHERE serviceStatus = %s " \
                        "AND name LIKE %s AND idCity = %s;"
            else:
                if criterion == "minimalCost":
                    query = "SELECT idService, name, description, slogan, typeService, workingHours" \
                            ", minimalCost, maximumCost, idMemberATE, idCity FROM Service WHERE serviceStatus = %s " \
                            "AND minimalCost = %s AND idCity = %s;"
                else:
                    if criterion == "maximumCost":
                        query = "SELECT idService, name, description, slogan, typeService, workingHours" \
                                ", minimalCost, maximumCost, idMemberATE, idCity FROM Service WHERE serviceStatus = %s " \
                                "AND maximumCost = %s AND idCity = %s;"
        param = [self.service_status, filter_search, self.id_city]
        if query is not None:
            list_services = self.connect.select(query, param)
            if list_services:
                services_list = []
                for services in list_services:
                    service = Service()
                    service.id_service = services["idService"]
                    service.name = services["name"]
                    service.description = services["description"]
                    service.slogan = services["slogan"]
                    service.type_service = services["typeService"]
                    service.working_hours = services["workingHours"]
                    service.minimal_cost = services["minimalCost"]
                    service.maximum_cost = services["maximumCost"]
                    service.id_city = services["idCity"]
                    service.id_memberATE = services["idMemberATE"]
                    services_list.append(service)
                results = services_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def get_services_city(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idService, name, description, slogan, typeService, workingHours, minimalCost, " \
                "maximumCost, idMemberATE, idCity FROM Service WHERE serviceStatus = %s AND idCity = %s "
        param = [self.service_status,
                 self.id_city]
        list_services = self.connect.select(query, param)
        if list_services:
            services_list = []
            for services in list_services:
                service = Service()
                service.id_service = services["idService"]
                service.name = services["name"]
                service.description = services["description"]
                service.slogan = services["slogan"]
                service.type_service = services["typeService"]
                service.working_hours = services["workingHours"]
                service.minimal_cost = services["minimalCost"]
                service.maximum_cost = services["maximumCost"]
                service.id_memberATE = services["idMemberATE"]
                service.id_city = services["idCity"]
                services_list.append(service)
            results = services_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def get_services_employee(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idService, name, description, slogan, typeService, workingHours, minimalCost, " \
                "maximumCost, idMemberATE, serviceStatus, idCity FROM Service WHERE idMemberATE = %s "
        param = [self.id_memberATE]
        list_services = self.connect.select(query, param)
        if list_services:
            services_list = []
            for services in list_services:
                service = Service()
                service.id_service = services["idService"]
                service.name = services["name"]
                service.description = services["description"]
                service.slogan = services["slogan"]
                service.type_service = services["typeService"]
                service.working_hours = services["workingHours"]
                service.minimal_cost = services["minimalCost"]
                service.maximum_cost = services["maximumCost"]
                service.id_memberATE = services["idMemberATE"]
                service.service_status = services["serviceStatus"]
                service.id_city = services["idCity"]
                services_list.append(service)
            results = services_list
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_service(self):
        return {"idService": self.id_service, "idMemberATE": self.id_memberATE, "name": self.name,
                "description": self.description, "slogan": self.slogan, "typeService": self.type_service,
                "idCity": self.id_city, "workingHours": self.working_hours, "serviceStatus": self.service_status,
                "minimalCost": self.minimal_cost, "maximumCost": self.maximum_cost}
