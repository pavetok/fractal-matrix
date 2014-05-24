# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import core
from .. import db
from ..models import Aspect, Universum, generate_aspects, generate_universums
from .forms import AspectForm


@core.route('/gena')
def gena():
    generate_aspects()
    return redirect(url_for('.index'))

@core.route('/genu')
def genu():
    generate_universums()
    return redirect(url_for('.index'))

@core.route('/', methods=['GET', 'POST'])
def index():
    # обрабатываем форму
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect(name=form.name.data)
        db.session.add(aspect)
        flash('Аспект был добавлен')
        return redirect(url_for('.index'))
    # отображаем таблицу
    universums = Universum.query.all()
    first_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 0)
    second_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 1)
    superaspects = Aspect.query.filter_by(superaspect_id=None)
    if len(list(superaspects)) == 2:
        (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
        return render_template('index.html',
                               form=form,
                               x_aspects=reversed(x_aspects),
                               y_aspects=y_aspects,
                               first_row_of_universums=first_row_of_universums,
                               second_row_of_universums=second_row_of_universums)
    else:
        return render_template('index.html', form=form)