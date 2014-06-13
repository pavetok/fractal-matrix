# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import tables
from ... import db
from ..models import Table
from .forms import TableForm


@tables.route('/tables')
@tables.route('/tables/<int:table_id>')
def get(table_id=None):
    if table_id is None:
        tables = Table.query.all()
        return render_template('tables/get.html', tables=tables)
    else:
        table = Table.query.get_or_404(table_id)
        return render_template('tables/get_by_id.html', table=table)

@tables.route('/tables/create', methods=['GET', 'POST'])
def create():
    form = TableForm()
    if form.validate_on_submit():
        table = Table(name=form.name.data)
        db.session.add(table)
        db.session.commit()
        flash('Таблица была создана')
        table = Table.query.filter_by(name=table.name).first()
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