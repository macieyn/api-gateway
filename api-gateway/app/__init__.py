from flask import Flask, jsonify, request
from requests.exceptions import ConnectionError
import requests
import json
import os

from app.auth import login_required


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    # create and configure the app
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'gateway.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return {'ok': True}, 200

    @app.route('/info')
    def info():
        return {'name': 'gateway'}, 200

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import service
    app.register_blueprint(service.bp)

    return app
