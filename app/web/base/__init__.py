# -*- coding:utf-8 -*-
from flask import Blueprint


base = Blueprint('base',
                 __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/web/base/static')

from . import views