# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import tables
from ... import db
from ..models import Table, Aspect
from .forms import TableForm


@tables.route('/tables')
@tables.route('/tables/<int:table_id>')
def get(table_id=None):
    if table_id is None:
        tables = Table.query.all()
        return render_template('tables/get.html', tables=tables)
    else:
        table = Table.query.get_or_404(table_id)
        universums = list(table.universums)
        first_row_of_universums = (universum for universum in universums if \
                                   universums.index(universum) % 2 == 0)
        second_row_of_universums = (universum for universum in universums if \
                                    universums.index(universum) % 2 == 1)
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        if len(list(superaspects)) == 2:
            (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
            return render_template('tables/get_by_id.html',
                                   table=table,
                                   x_aspects=reversed(x_aspects),
                                   y_aspects=y_aspects,
                                   first_row_of_universums=reversed(list(first_row_of_universums)),
                                   second_row_of_universums=reversed(list(second_row_of_universums)))
        else:
            return render_template('tables/get_by_id.html', table=table)

@tables.route('/tables/create', methods=['GET', 'POST'])
def create():
    form = TableForm()
    if form.validate_on_submit():
        table = Table(name=form.name.data)
        db.session.add(table)
        db.session.commit()
        flash('Таблица была создана')
        table = Table.query.get_or_404(table.id)
        return redirect(url_for('.get', table_id=table.id))
    return render_template('tables/create.html', form=form)

@tables.route('/tables/<int:table_id>/update', methods=['GET', 'POST'])
def update(table_id):
    table = Table.query.get_or_404(table_id)
    form = TableForm()
    if form.validate_on_submit():
        table.name = form.name.data
        db.session.commit()
        flash('Таблица была изменена')
        return redirect(url_for('.get', table_id=table.id))
    form.name.data = table.name
    return render_template('tables/update.html', form=form)

@tables.route('/tables/<int:table_id>/delete', methods=['GET', 'POST'])
def delete(table_id):
    table = Table.query.get_or_404(table_id)
    db.session.delete(table)
    flash('Таблица была удалена')
    return redirect(url_for('.get'))