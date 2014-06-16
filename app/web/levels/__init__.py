# -*- coding:utf-8 -*-
from flask import Blueprint


levels = Blueprint('levels', __name__)


from . import views