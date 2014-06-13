# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import tables
from .. import db
from .models import Table
from .forms import BaseEntityForm


@tables.route('')
@tables.route('/<int:id>')
def get(id=None):
    if id is None:
        tables = Table.query.all()
        return render_template('tables/get.html', tables=tables)
    else:
        table = Table.query.get_or_404(id)
        return render_template('tables/get_by_id.html', table=table)

@tables.route('/create', methods=['GET', 'POST'])
def create():
    form = BaseEntityForm()
    if form.validate_on_submit():
        table = Table(name=form.name.data)
        db.session.add(table)
        db.session.commit()
        flash('Таблица была создана')
        table = Table.query.filter_by(name=table.name).first()
        return redirect(url_for('.get', id=table.id))
    return render_template('tables/create.html', form=form)

@tables.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    table = Table.query.get_or_404(id)
    form = BaseEntityForm()
    if form.validate_on_submit():
        table.name = form.name.data
        db.session.commit()
        flash('Таблица была изменена')
        return redirect(url_for('.get', id=table.id))
    form.name.data = table.name
    return render_template('tables/update.html', form=form)

@tables.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    table = Table.query.get_or_404(id)
    db.session.delete(table)
    flash('Таблица была удалена')
    return redirect(url_for('.get'))