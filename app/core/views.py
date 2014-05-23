# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import core
from .. import db
from ..models import Aspect, Universum
from .forms import AspectForm


@core.route('/', methods=['GET', 'POST'])
def index():
    # aspects = Aspect.query.all()
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect()
        aspect.name = form.name.data
        db.session.add(aspect)
        flash('Аспект был добавлен')
        return redirect(url_for('.index'))
    return render_template('index.html', form=form)