# -*- coding:utf-8 -*-
from flask import Blueprint


core = Blueprint('core',
                 __name__,
                 template_folder='templates',
                 static_folder='static',
                 static_url_path='/core/static')

from . import views