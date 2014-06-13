# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import dimensions
from ... import db
from ..models import Table, Dimension, Aspect
from .forms import DimensionForm


@dimensions.route('/tables/<int:table_id>/dimensions')
@dimensions.route('/tables/<int:table_id>/dimensions/<int:dimension_id>')
def get(table_id, dimension_id=None):
    table = Table.query.get_or_404(table_id)
    if dimension_id is None:
        return render_template('dimensions/get.html', table=table)
    else:
        dimension = Dimension.query.get_or_404(dimension_id)
        return render_template('dimensions/get_by_id.html', table=table,
                               dimension=dimension)


@dimensions.route('/tables/<int:table_id>/dimensions/create',
                  methods=['GET', 'POST'])
def create(table_id):
    form = DimensionForm()
    superaspects = Aspect.query.filter_by(superaspect=None).order_by('name')
    form.aspect.choices = [(aspect.id, aspect.name) for aspect in superaspects]
    if form.validate_on_submit():
        dimension = Dimension(name=form.name.data)
        dimension.table = Table.query.get_or_404(table_id)
        dimension.aspect = Aspect.query.get(form.aspect.data)
        db.session.add(dimension)
        db.session.commit()
        flash('Измерение было создано')
        return redirect(url_for('.get', table_id=table_id,
                                dimension_id=dimension.id))
    return render_template('dimensions/create.html', form=form)


@dimensions.route('/tables/<int:table_id>/dimensions/<int:dimension_id>/update',
                  methods=['GET', 'POST'])
def update(table_id, dimension_id):
    form = DimensionForm()
    dimension = Dimension.query.get_or_404(dimension_id)
    superaspects = Aspect.query.filter_by(superaspect=None).order_by('name')
    form.aspect.choices = [(aspect.id, aspect.name) for aspect in superaspects]
    form.aspect.data = dimension.aspect.id
    if form.validate_on_submit():
        dimension.name = form.name.data
        dimension.aspect = Aspect.query.get(form.aspect.data)
        db.session.commit()
        flash('Измерение было изменено')
        return redirect(url_for('.get', table_id=table_id,
                                dimension_id=dimension_id))
    form.name.data = dimension.name
    return render_template('dimensions/update.html', form=form)


@dimensions.route('/tables/<int:table_id>/dimensions/<int:dimension_id>/delete',
                  methods=['GET', 'POST'])
def delete(table_id, dimension_id):
    dimension = Dimension.query.get_or_404(dimension_id)
    db.session.delete(dimension)
    flash('Измерение было удалено')
    return redirect(url_for('.get', table_id=table_id))