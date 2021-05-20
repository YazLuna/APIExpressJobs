from flask import Blueprint

report = Blueprint("Reports", __name__)


@report.route("/reports", methods=["POST"])
def add_report(body, report=None):  # noqa: E501
    """Add a new report to the report catalog

    Add new report # noqa: E501

    :param body: Report object that needs to be added to the catalog
    :type body: dict | bytes
    :param report: The report to create
    :type report: dict | bytes

    :rtype: None
    """
    return 'do some magic!'


@report.route("/reports/{reportId}", methods=["GET"])
def get_report_by_id(report_id):  # noqa: E501
    """Returns a single report

    Find report by ID # noqa: E501

    :param report_id: ID of report to return
    :type report_id: int

    :rtype: Report
    """
    return 'do some magic!'


@report.route("/reports", methods=["GET"])
def get_reports(filter):  # noqa: E501
    """Returns a list of reports

    Returns a list of reports made to services # noqa: E501

    :param filter: 
    :type filter: str

    :rtype: InlineResponse200
    """
    return 'do some magic!'
