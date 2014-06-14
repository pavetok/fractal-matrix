# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import base


@base.route('/')
def index():
    return redirect(url_for('tables.get'))