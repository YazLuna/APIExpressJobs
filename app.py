from flask_cors import CORS
from flask import Flask

from src.routes.servicesATE import serviceATE
from src.routes.memberATE import memberATE

app = Flask(__name__)
CORS(app)
app.register_blueprint(serviceATE)
app.register_blueprint(memberATE)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
