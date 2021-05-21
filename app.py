from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from src.routes.account_controller import account
from src.routes.emails_controller import email
from src.routes.employees_controller import employee
from src.routes.login import login
from src.routes.messages_controller import message
from src.routes.ratings_controller import rating
from src.routes.reports_controller import report
from src.routes.requests_controller import request
from src.routes.resources_controller import resource
from src.routes.services_controller import service

app = Flask(__name__)
CORS(app)
app.register_blueprint(account)
app.register_blueprint(email)
app.register_blueprint(employee)
app.register_blueprint(message)
app.register_blueprint(rating)
app.register_blueprint(report)
app.register_blueprint(request)
app.register_blueprint(resource)
app.register_blueprint(service)
app.register_blueprint(login)
app.config["SECRET_KEY"] = "gettawi777stb"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
