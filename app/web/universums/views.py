# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import universums
from ... import db
from ..models import Matrix, Level, Aspect, Universum
from .forms import UniversumSimpleForm, UniversumFullForm


@universums.route('/matrices/<int:matrix_id>/universums')
@universums.route('/matrices/<int:matrix_id>/universums/')
@universums.route('/matrices/<int:matrix_id>/universums/<int:universum_id>')
def get(matrix_id, universum_id=None):
    matrix = Matrix.query.get_or_404(matrix_id)
    if universum_id is None:
        return render_template('universums/get_all.html', matrix=matrix)
    else:
        universum = Universum.query.get_or_404(universum_id)
        return render_template('universums/get_one.html', matrix=matrix,
                               universum=universum)

@universums.route('/matrices/<int:matrix_id>/universums/create',
                  methods=['GET', 'POST'])
def create(matrix_id):
    form = UniversumFullForm()
    matrix = Matrix.query.get_or_404(matrix_id)
    form.level.choices = [(level.id, level.value) for level in matrix.levels]
    form.aspects.choices = [(aspect.id, aspect.name) \
                            for aspect in matrix.aspects]
    if form.validate_on_submit():
        universum = Universum(name=form.name.data)
        universum.matrix = matrix
        universum.level = Level.query.get(form.level.data)
        universum.aspects.extend(Aspect.query.get(aspect_id) \
                                 for aspect_id in form.aspects.data)
        db.session.add(universum)
        flash('Универсум был создан')
        return redirect(url_for('.get', matrix_id=matrix_id,
                                universum_id=universum.id))
    return render_template('universums/create.html', form=form)

@universums.route('/matrices/<int:matrix_id>/universums/<int:universum_id>/update',
                  methods=['GET', 'POST'])
def update(matrix_id, universum_id):
    form = UniversumSimpleForm()
    universum = Universum.query.get_or_404(universum_id)
    if form.validate_on_submit():
        universum.name = form.name.data
        flash('Универсум был изменен')
        return redirect(url_for('.get', matrix_id=matrix_id))
    form.name.data = universum.name
    return render_template('universums/update.html', form=form)

@universums.route('/matrices/<int:matrix_id>/universums/<int:universum_id>/delete',
                  methods=['GET', 'POST'])
def delete(matrix_id, universum_id):
    universum = Universum.query.get_or_404(universum_id)
    db.session.delete(universum)
    flash('Универсум был удален')
    return redirect(url_for('.get', matrix_id=matrix_id))