# -*- coding:utf-8 -*-
from flask import url_for, redirect
from . import levels
from ... import db
from ..models import Matrix, Level


@levels.route('/matrices/<int:matrix_id>/levels/<int:level_value>/generate')
def generate(matrix_id, level_value):
    matrix = Matrix.query.get_or_404(matrix_id)
    new_level = Level(value=level_value, matrix=matrix)
    matrix.generate(new_level)
    return redirect(url_for('matrices.get', matrix_id=matrix.id, level_id=new_level.id))


@levels.route('/matrices/<int:matrix_id>/levels/<int:level_id>/delete')
def delete(matrix_id, level_id):
    level = Level.query.get_or_404(level_id)
    db.session.delete(level)
    return redirect(url_for('matrices.get', matrix_id=matrix_id, level_id=level.prev.id))