# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from .. import tables
from ... import db
from ..models import Table, Aspect
from ..forms import BaseEntityForm


@tables.route('/<int:table_id>/aspects')
@tables.route('/<int:table_id>/aspects/<int:aspect_id>')
def get(table_id, aspect_id=None):
    if aspect_id is None:
        table = Table.query.get_or_404(table_id)
        return render_template('aspects/get.html', aspects=table.aspects)
    else:
        aspect = Aspect.query.get_or_404(aspect_id)
        return render_template('aspects/get_by_id.html', aspect=aspect)

@tables.route('/<int:table_id>/aspects/create', methods=['GET', 'POST'])
def create(table_id):
    form = BaseEntityForm()
    if form.validate_on_submit():
        table = Table.query.get_or_404(table_id)
        aspect = Aspect(name=form.name.data)
        table.aspects.append(aspect)
        db.session.add(table)
        db.session.commit()
        flash('Аспект был создан')
        aspect = Aspect.query.get_or_404(aspect.id)
        return redirect(url_for('.get', table_id=table.id, aspect_id=aspect.id))
    return render_template('aspects/create.html', form=form)

@tables.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    aspect = Aspect.query.get_or_404(id)
    form = BaseEntityForm()
    if form.validate_on_submit():
        aspect.name = form.name.data
        db.session.commit()
        flash('Аспект был изменен')
        return redirect(url_for('.get', id=aspect.id))
    form.name.data = aspect.name
    return render_template('aspects_update.html', form=form)

@tables.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    aspect = Aspect.query.get_or_404(id)
    db.session.delete(aspect)
    flash('Аспект был удален')
    return redirect(url_for('.get'))