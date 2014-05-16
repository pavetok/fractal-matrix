# -*- coding:utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    bootstrap.init_app(app)

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)

    return app