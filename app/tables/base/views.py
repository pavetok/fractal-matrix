# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from .. import tables
from ... import db
from ..models import Aspect, Universum, generate_aspects, generate_universums


@tables.route('/gena')
def gena():
    superaspects = Aspect.query.filter_by(superaspect_id=None)
    generate_aspects(superaspects)
    return redirect(url_for('.index'))

@tables.route('/genu')
def genu():
    superaspects = Aspect.query.filter_by(superaspect_id=None)
    generate_universums(superaspects)
    return redirect(url_for('.index'))

@tables.route('/')
def index():
    universums = Universum.query.all()
    first_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 0)
    second_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 1)
    superaspects = Aspect.query.filter_by(superaspect_id=None)
    if len(list(superaspects)) == 2:
        (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
        return render_template('index.html',
                               x_aspects=reversed(x_aspects),
                               y_aspects=y_aspects,
                               first_row_of_universums=reversed(list(first_row_of_universums)),
                               second_row_of_universums=reversed(list(second_row_of_universums)))
    else:
        return render_template('index.html')