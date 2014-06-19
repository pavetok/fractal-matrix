# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import aspects
from ... import db
from ..models import Matrix, Aspect
from .forms import AspectForm


@aspects.route('/matrices/<int:matrix_id>/aspects')
@aspects.route('/matrices/<int:matrix_id>/aspects/')
@aspects.route('/matrices/<int:matrix_id>/aspects/<int:aspect_id>')
def get(matrix_id, aspect_id=None):
    matrix = Matrix.query.get_or_404(matrix_id)
    if aspect_id is None:
        return render_template('aspects/get_all.html', matrix=matrix)
    else:
        aspect = Aspect.query.get_or_404(aspect_id)
        return render_template('aspects/get_one.html', matrix=matrix,
                               aspect=aspect)


@aspects.route('/matrices/<int:matrix_id>/aspects/create',
               methods=['GET', 'POST'])
def create(matrix_id):
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect(name=form.name.data)
        aspect.matrix = Matrix.query.get_or_404(matrix_id)
        db.session.add(aspect)
        db.session.commit()
        flash('Аспект был создан')
        return redirect(url_for('.get', matrix_id=matrix_id))
    return render_template('aspects/create.html', form=form)


@aspects.route('/matrices/<int:matrix_id>/aspects/<int:aspect_id>/update',
               methods=['GET', 'POST'])
def update(matrix_id, aspect_id):
    form = AspectForm()
    aspect = Aspect.query.get_or_404(aspect_id)
    if form.validate_on_submit():
        aspect.name = form.name.data
        db.session.commit()
        flash('Аспект был изменен')
        return redirect(url_for('.get', matrix_id=matrix_id,
                                aspect_id=aspect_id))
    form.name.data = aspect.name
    return render_template('aspects/update.html', form=form)


@aspects.route('/matrices/<int:matrix_id>/aspects/<int:aspect_id>/delete',
               methods=['GET', 'POST'])
def delete(matrix_id, aspect_id):
    aspect = Aspect.query.get_or_404(aspect_id)
    db.session.delete(aspect)
    flash('Аспект был удален')
    return redirect(url_for('.get', matrix_id=matrix_id))