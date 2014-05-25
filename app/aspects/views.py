# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import aspects
from .. import db
from ..models import Aspect
from .forms import AspectForm


@aspects.route('/get', methods=['GET'])
def get():
    aspects = Aspect.query.all()
    return render_template('aspects_get.html', aspects=aspects)

@aspects.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    aspect = Aspect.query.get_or_404(id)
    return render_template('aspects_get_by_id.html', aspect=aspect)

@aspects.route('/add', methods=['GET', 'POST'])
def add():
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect(name=form.name.data)
        db.session.add(aspect)
        flash('Аспект был добавлен')
        return redirect(url_for('.get_by_id', id=aspect.id))
    return render_template('aspects_add.html', form=form)

@aspects.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    aspect = Aspect.query.get_or_404(id)
    form = AspectForm()
    if form.validate_on_submit():
        aspect.name = form.name.data
        db.session.commit()
        flash('Аспект был изменен')
        return redirect(url_for('.get_by_id', id=aspect.id))
    form.name.data = aspect.name
    return render_template('aspects_upd.html', form=form)

@aspects.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    aspect = Aspect.query.get_or_404(id)
    db.session.delete(aspect)
    flash('Аспект был удален')
    return redirect(url_for('.get'))