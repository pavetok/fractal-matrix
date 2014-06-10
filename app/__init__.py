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

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)

    from .dimensions import dimensions as dimensions_blueprint
    app.register_blueprint(dimensions_blueprint, url_prefix='/dimensions')

    from .aspects import aspects as aspects_blueprint
    app.register_blueprint(aspects_blueprint, url_prefix='/aspects')

    from .universums import universums as universums_blueprint
    app.register_blueprint(universums_blueprint, url_prefix='/universums')

    return app