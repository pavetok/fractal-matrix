# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import matrices
from ... import db
from ..models import Matrix, Level, Aspect
from .forms import MatrixForm


@matrices.route('/matrices')
@matrices.route('/matrices/')
@matrices.route('/matrices/<int:matrix_id>')
@matrices.route('/matrices/<int:matrix_id>/levels/<int:level_id>')
def get(matrix_id=None, level_id=1):
    if matrix_id is None:
        matrices = Matrix.query.all()
        return render_template('matrices/get_all.html', matrices=matrices)
    matrix = Matrix.query.get_or_404(matrix_id)
    level = Level.query.get_or_404(level_id)
    return render_template('matrices/get_one.html', matrix=matrix, level=level)


@matrices.route('/matrices/create', methods=['GET', 'POST'])
def create():
    form = MatrixForm()
    if form.validate_on_submit():
        matrix = Matrix(name=form.name.data)
        db.session.add(matrix)
        db.session.commit()
        flash('Матрица была создана')
        matrix = Matrix.query.get_or_404(matrix.id)
        return redirect(url_for('.get', matrix_id=matrix.id))
    return render_template('matrices/create.html', form=form)

@matrices.route('/matrices/<int:matrix_id>/update', methods=['GET', 'POST'])
def update(matrix_id):
    matrix = Matrix.query.get_or_404(matrix_id)
    form = MatrixForm()
    if form.validate_on_submit():
        matrix.name = form.name.data
        db.session.commit()
        flash('Матрица была изменена')
        return redirect(url_for('.get', matrix_id=matrix.id))
    form.name.data = matrix.name
    return render_template('matrices/update.html', form=form)

@matrices.route('/matrices/<int:matrix_id>/delete', methods=['GET', 'POST'])
def delete(matrix_id):
    matrix = Matrix.query.get_or_404(matrix_id)
    db.session.delete(matrix)
    flash('Матрица была удалена')
    return redirect(url_for('.get'))