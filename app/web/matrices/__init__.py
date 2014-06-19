# -*- coding:utf-8 -*-
from flask import Blueprint


matrices = Blueprint('matrices',
                     __name__,
                     template_folder='templates',
                     static_folder='static/css',
                     static_url_path='/web/matrices/static')

from . import views