from datetime import timedelta, date

from flask import Flask
from flask_cors import CORS

from src.routes.account_controller import account
from src.routes.chats_controller import chat
from src.routes.cities_controller import city
from src.routes.countries_controller import country
from src.routes.emails_controller import email
from src.routes.employees_controller import employee
from src.routes.images_controller import image
from src.routes.login_controller import login
from src.routes.messages_controller import message
from src.routes.ratings_controller import rating
from src.routes.reports_controller import report
from src.routes.requests_controller import requestService
from src.routes.resources_controller import resource
from src.routes.services_controller import service
from src.routes.states_controller import state

app = Flask(__name__)
CORS(app)
app.register_blueprint(account)
app.register_blueprint(email)
app.register_blueprint(employee)
app.register_blueprint(message)
app.register_blueprint(rating)
app.register_blueprint(report)
app.register_blueprint(requestService)
app.register_blueprint(resource)
app.register_blueprint(service)
app.register_blueprint(login)
app.register_blueprint(chat)
app.register_blueprint(city)
app.register_blueprint(country)
app.register_blueprint(state)
app.register_blueprint(image)
app.config["SECRET_KEY"] = "gettawi777stb"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
