from flask import Blueprint

report = Blueprint("report", __name__)


@report.route("/reports", methods=["POST"])
def add_report():
    pass

