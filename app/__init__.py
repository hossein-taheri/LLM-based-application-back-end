from flask import Flask
from flask_cors import CORS

from . import bootstrap
from .blueprints.home import home
from .blueprints.auth import auth
from .blueprints.chat import chat


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(chat, url_prefix='/chat')

    return app
