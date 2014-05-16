# -*- coding:utf-8 -*-
from flask import render_template
from . import core


@core.route('/')
def index():
    return render_template('base.html')