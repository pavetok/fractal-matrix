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
        return render_template('matrices/get.html', matrices=matrices)
    else:
        matrix = Matrix.query.get_or_404(matrix_id)
        level = Level.query.get_or_404(level_id)
        universums = matrix.universums.all()
        first_row_of_universums = (universum for universum in universums if \
                                   universums.index(universum) % 2 == 0)
        second_row_of_universums = (universum for universum in universums if \
                                    universums.index(universum) % 2 == 1)
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        if len(list(superaspects)) == 2:
            (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
            return render_template('matrices/get_by_id.html',
                                   matrix=matrix,
                                   level=level,
                                   x_aspects=reversed(x_aspects),
                                   y_aspects=y_aspects,
                                   first_row_of_universums=reversed(list(first_row_of_universums)),
                                   second_row_of_universums=reversed(list(second_row_of_universums)))
        else:
            return render_template('matrices/get_by_id.html',
                                   matrix=matrix,
                                   level=level)

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