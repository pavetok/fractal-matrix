# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import base
from ..models import Aspect, Universum


@base.route('/')
def index():
    universums = Universum.query.all()
    first_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 0)
    second_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 1)
    superaspects = Aspect.query.filter_by(superaspect_id=None)
    if len(list(superaspects)) == 2:
        (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
        return render_template('base/index.html',
                               x_aspects=reversed(x_aspects),
                               y_aspects=y_aspects,
                               first_row_of_universums=reversed(list(first_row_of_universums)),
                               second_row_of_universums=reversed(list(second_row_of_universums)))
    else:
        return render_template('base/index.html')