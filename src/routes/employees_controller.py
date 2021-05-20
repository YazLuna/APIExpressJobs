from flask import Blueprint

employee = Blueprint("Employees", __name__)


@employee.route("/employees", methods=["POST"])
def add_employee_account():
    pass
