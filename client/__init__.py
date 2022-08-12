# setup for flask app
from flask import Flask, app
from os import path

# creates the flask app
def create_app():
    app = Flask(__name__)

    # import blueprints
    from .auth import auth

    app.register_blueprint(auth, url_prefix='/')

    return app
