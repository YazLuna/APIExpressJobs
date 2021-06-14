"""This module manages the reports."""
import json

from flask import Blueprint, request, Response

from src.models.account_role import AccountRole
from src.models.report import Report
from src.routes.auth import Auth
from src.routes.exception_responses_json import json_error
from src.routes.responses_rest import ResponsesREST
from src.validators.validators import validator_report, validator_id, validator_get_reports

report = Blueprint("Reports", __name__)


@report.route("/reports", methods=["POST"])
@Auth.requires_token
@Auth.requires_role(AccountRole.CLIENT.name)
def add_report():
    """This function add a report a service."""
    json_values = request.json
    values_required = {"reason", "idService", "idMemberATE"}
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if all(key in json_values for key in values_required):
        if validator_report.is_valid(json_values):
            report_add = Report()
            report_add.reason = json_values["reason"]
            report_add.id_service = json_values["idService"]
            report_add.id_member_ate = json_values["idMemberATE"]
            result = report_add.add_report()
            if result == ResponsesREST.CREATED.value:
                response = Response(json.dumps(report_add.json_report()),
                                    status=ResponsesREST.CREATED.value,
                                    mimetype="application/json")
            else:
                response = Response(json.dumps(json_error(result)),
                                    status=result, mimetype="application/json")
    return response


@report.route("/reports/<report_id>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.MANAGER.name)
def get_report_by_id(report_id):
    """This function get a report according to its ID."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_id.is_valid({"id": report_id}):
        report_get = Report()
        report_get.id_report = report_id
        result = report_get.consult_report()
        if result in (ResponsesREST.NOT_FOUND.value, ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            response = Response(json.dumps(result.json_report()),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response


@report.route("/reports/<filter_search>/<criterion>", methods=["GET"])
@Auth.requires_token
@Auth.requires_role(AccountRole.MANAGER.name)
def get_reports(filter_search, criterion):
    """This function get a report according to criterion: memberATE, service, date ."""
    response = Response(json.dumps(json_error(ResponsesREST.INVALID_INPUT.value)),
                        status=ResponsesREST.INVALID_INPUT.value, mimetype="application/json")
    if validator_get_reports.is_valid({"filterSearch": filter_search, "criterion": criterion}):
        get_report = Report()
        result = get_report.consult_list_reports(filter_search, criterion)
        if result in (ResponsesREST.INVALID_INPUT.value, ResponsesREST.NOT_FOUND.value,
                      ResponsesREST.SERVER_ERROR.value):
            response = Response(json.dumps(json_error(result)),
                                status=result, mimetype="application/json")
        else:
            list_reports = []
            for reports_found in result:
                list_reports.append(reports_found.json_report())
            response = Response(json.dumps(list_reports),
                                status=ResponsesREST.SUCCESSFUL.value,
                                mimetype="application/json")
    return response
