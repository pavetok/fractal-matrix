# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)

    from .web import base_blueprint, matrices_blueprint, dimensions_blueprint, \
        aspects_blueprint, universums_blueprint, levels_blueprint
    app.register_blueprint(base_blueprint)
    app.register_blueprint(matrices_blueprint)
    app.register_blueprint(dimensions_blueprint)
    app.register_blueprint(aspects_blueprint)
    app.register_blueprint(universums_blueprint)
    app.register_blueprint(levels_blueprint)

    return app