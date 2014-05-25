# -*- coding:utf-8 -*-
from flask import Blueprint


aspects = Blueprint('aspects',
                    __name__,
                    template_folder='templates')

from . import views