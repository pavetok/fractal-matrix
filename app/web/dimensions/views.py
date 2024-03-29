# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import dimensions
from ... import db
from ..models import Matrix, Dimension, Aspect
from .forms import DimensionForm


@dimensions.route('/matrices/<int:matrix_id>/dimensions')
@dimensions.route('/matrices/<int:matrix_id>/dimensions/')
@dimensions.route('/matrices/<int:matrix_id>/dimensions/<int:dimension_id>')
def get(matrix_id, dimension_id=None):
    matrix = Matrix.query.get_or_404(matrix_id)
    if dimension_id is None:
        return render_template('dimensions/get_all.html', matrix=matrix)
    else:
        dimension = Dimension.query.get_or_404(dimension_id)
        return render_template('dimensions/get_one.html', matrix=matrix,
                               dimension=dimension)


@dimensions.route('/matrices/<int:matrix_id>/dimensions/create',
                  methods=['GET', 'POST'])
def create(matrix_id):
    form = DimensionForm()
    superaspects = Aspect.query.filter_by(superaspect=None)
    form.aspect.choices = [(aspect.id, aspect.name) for aspect in superaspects]
    if form.validate_on_submit():
        dimension = Dimension(name=form.name.data)
        dimension.matrix = Matrix.query.get_or_404(matrix_id)
        dimension.aspect = Aspect.query.get(form.aspect.data)
        dimension.type = form.type.data
        db.session.add(dimension)
        db.session.commit()
        flash('Измерение было создано')
        return redirect(url_for('.get', matrix_id=matrix_id))
    return render_template('dimensions/create.html', form=form)


@dimensions.route('/matrices/<int:matrix_id>/dimensions/<int:dimension_id>/update',
                  methods=['GET', 'POST'])
def update(matrix_id, dimension_id):
    form = DimensionForm()
    dimension = Dimension.query.get_or_404(dimension_id)
    superaspects = Aspect.query.filter_by(superaspect=None)
    form.aspect.choices = [(aspect.id, aspect.name) for aspect in superaspects]
    form.aspect.data = dimension.aspect.id
    if form.validate_on_submit():
        dimension.name = form.name.data
        dimension.aspect = Aspect.query.get(form.aspect.data)
        dimension.type = form.type.data
        db.session.commit()
        flash('Измерение было изменено')
        return redirect(url_for('.get', matrix_id=matrix_id,
                                dimension_id=dimension_id))
    form.name.data = dimension.name
    return render_template('dimensions/update.html', form=form)


@dimensions.route('/matrices/<int:matrix_id>/dimensions/<int:dimension_id>/delete',
                  methods=['GET', 'POST'])
def delete(matrix_id, dimension_id):
    dimension = Dimension.query.get_or_404(dimension_id)
    db.session.delete(dimension)
    flash('Измерение было удалено')
    return redirect(url_for('.get', matrix_id=matrix_id))