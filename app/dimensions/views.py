# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import dimensions
from .. import db
from ..models import Dimension, Aspect
from .forms import DimensionForm


@dimensions.route('')
@dimensions.route('/<int:id>')
def get(id=None):
    if id is None:
        dimensions = Dimension.query.all()
        return render_template('dimensions_get.html', dimensions=dimensions)
    else:
        dimension = Dimension.query.get_or_404(id)
        return render_template('dimensions_get_by_id.html', dimension=dimension)

@dimensions.route('/add', methods=['GET', 'POST'])
def add():
    form = DimensionForm()
    superaspects = Aspect.query.filter_by(superaspect=None).order_by('name')
    form.aspect.choices = [(aspect.id, aspect.name) for aspect in superaspects]
    if form.validate_on_submit():
        dimension = Dimension(name=form.name.data,
                              aspect=Aspect.query.get(form.aspect.data))
        db.session.add(dimension)
        db.session.commit()
        flash('Измерение было добавлено')
        dimension = Dimension.query.filter_by(name=dimension.name).first()
        return redirect(url_for('.get', id=dimension.id))
    return render_template('dimensions_add.html', form=form)

@dimensions.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = DimensionForm()
    dimension = Dimension.query.get_or_404(id)
    superaspects = Aspect.query.filter_by(superaspect=None).order_by('name')
    form.aspect.choices = [(aspect.id, aspect.name) for aspect in superaspects]
    form.aspect.data = dimension.aspect.id
    if form.validate_on_submit():
        dimension.name = form.name.data
        dimension.aspect = Aspect.query.get(form.aspect.data)
        db.session.commit()
        flash('Измерение было изменено')
        return redirect(url_for('.get', id=dimension.id))
    form.name.data = dimension.name
    return render_template('dimensions_update.html', form=form)

@dimensions.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    dimension = Dimension.query.get_or_404(id)
    db.session.delete(dimension)
    flash('Измерение было удалено')
    return redirect(url_for('.get'))