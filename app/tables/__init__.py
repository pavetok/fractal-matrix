# -*- coding:utf-8 -*-
from flask import Blueprint


tables = Blueprint('tables',
                   __name__,
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/tables/static')

from . import views