# -*- coding:utf-8 -*-
from flask import Blueprint


universums = Blueprint('universums',
                       __name__,
                       template_folder='templates')

from . import views