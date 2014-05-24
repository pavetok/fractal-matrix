# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import core
from .. import db
from ..models import Aspect, Universum
from .forms import AspectForm


@core.route('/', methods=['GET', 'POST'])
def index():
    # обрабатываем форму
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect()
        aspect.name = form.name.data
        db.session.add(aspect)
        flash('Аспект был добавлен')
        return redirect(url_for('.index'))
    # отображаем таблицу
    # aspects = Aspect.query.filter_by(subaspect_id=None)
    return render_template('index.html', form=form)