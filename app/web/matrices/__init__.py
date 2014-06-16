# -*- coding:utf-8 -*-
from flask import Blueprint


matrices = Blueprint('matrices',
                     __name__,
                     template_folder='templates')

from . import views