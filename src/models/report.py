from datetime import date

from src.connect_database.Connection import Connection
from src.routes.responses_rest import ResponsesREST


def getDate():
    today = date.today()
    return today.strftime("%Y/%m/%d")


class Report:
    def __init__(self):
        self.id_report = 0
        self.reason = ""
        self.id_service = 0
        self.id_memberATE = 0
        self.date = getDate()
        self.connect = Connection.build_from_static()

    def convert_date(self):
        self.date = self.date.strftime('%Y/%m/%d')

    def add_report(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "INSERT INTO Report (idMemberATE, reason, idService, date) VALUES (%s, %s, %s, %s); "
        param = [self.id_memberATE,
                 self.reason,
                 self.id_service,
                 self.date]
        result = self.connect.send_query(query, param)
        if result:
            self.id_report = self.get_id()
            results = ResponsesREST.CREATED.value
        return results

    def get_id(self):
        query = "SELECT idReport FROM Report order by idReport desc limit 1;"
        response = self.connect.select(query)
        report = Report()
        if response:
            id_list = response[0]
            report.id_report = id_list["idReport"]
        return report.id_report

    def consult_list_reports(self, filter_search, criterion):
        results = ResponsesREST.SERVER_ERROR.value
        query = None
        if criterion == "memberATE":
            query = "SELECT R.idReport, R.reason, S.name, MA.name AS nameMember, MA.lastName, " \
                    "R.date, R.idReport FROM Report R INNER JOIN Service S ON " \
                    "R.idService = S.idService INNER JOIN  MemberATE MA " \
                    "ON R.idMemberATE = MA.idMemberATE WHERE MA.name = %s;"
        else:
            if criterion == "service":
                query = "SELECT R.idReport, R.reason, S.name, MA.name AS nameMember, MA.lastName, " \
                        "R.date, R.idReport FROM Report R INNER JOIN Service S ON " \
                        "R.idService = S.idService INNER JOIN  MemberATE MA " \
                        "ON R.idMemberATE = MA.idMemberATE WHERE S.name = %s;"
            else:
                if criterion == "date":
                    query = "SELECT R.idReport, R.reason, S.name, MA.name AS nameMember, MA.lastName, " \
                            "R.date, R.idReport FROM Report R INNER JOIN Service S ON " \
                            "R.idService = S.idService INNER JOIN  MemberATE MA " \
                            "ON R.idMemberATE = MA.idMemberATE WHERE date = %s;"
        param = [filter_search]
        if query is not None:
            list_reports = self.connect.select(query, param)
            if list_reports:
                reports_list = []
                for reports in list_reports:
                    report = Report()
                    report.id_service = reports["name"]
                    report.reason = reports["reason"]
                    report.date = reports["date"]
                    report.date = report.date.strftime('%Y/%m/%d')
                    report.id_memberATE = reports["nameMember"] + " " + reports["lastName"]
                    report.id_report = reports["idReport"]
                    reports_list.append(report)
                results = reports_list
            else:
                results = ResponsesREST.NOT_FOUND.value
        else:
            results = ResponsesREST.INVALID_INPUT.value
        return results

    def consult_report(self):
        results = ResponsesREST.SERVER_ERROR.value
        query = "SELECT idMemberATE, reason, date, idService, idReport FROM Report WHERE idReport = %s"
        param = [self.id_report]
        reports = self.connect.select(query, param)
        if reports:
            report = Report()
            reports = reports[0]
            report.id_report = reports["idReport"]
            report.id_service = reports["idService"]
            report.reason = reports["reason"]
            report.date = reports["date"]
            report.date = report.date.strftime('%Y/%m/%d')
            report.id_memberATE = reports["idMemberATE"]
            results = report
        else:
            results = ResponsesREST.NOT_FOUND.value
        return results

    def json_report(self):
        return {"idReport": self.id_report, "reason": self.reason, "date": self.date,
                "idService": self.id_service, "idMemberATE": self.id_memberATE}
