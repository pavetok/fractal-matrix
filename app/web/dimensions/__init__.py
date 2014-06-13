# -*- coding:utf-8 -*-
from flask import Blueprint


dimensions = Blueprint('dimensions',
                       __name__,
                       template_folder='templates')

from . import views