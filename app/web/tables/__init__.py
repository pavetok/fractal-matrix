# -*- coding:utf-8 -*-
from flask import Blueprint


tables = Blueprint('tables',
                   __name__,
                   template_folder='templates')

from . import views