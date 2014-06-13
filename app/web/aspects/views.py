# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import aspects
from ... import db
from ..models import Table, Aspect
from .forms import AspectForm


@aspects.route('/tables/<int:table_id>/aspects/generate')
def generate(table_id):
    table = Table.query.get_or_404(table_id)
    Aspect.generate(table)
    return redirect(url_for('.get', table_id=table_id))


@aspects.route('/tables/<int:table_id>/aspects')
@aspects.route('/tables/<int:table_id>/aspects/<int:aspect_id>')
def get(table_id, aspect_id=None):
    table = Table.query.get_or_404(table_id)
    if aspect_id is None:
        return render_template('aspects/get.html', table=table)
    else:
        aspect = Aspect.query.get_or_404(aspect_id)
        return render_template('aspects/get_by_id.html', table=table,
                               aspect=aspect)


@aspects.route('/tables/<int:table_id>/aspects/create',
               methods=['GET', 'POST'])
def create(table_id):
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect(name=form.name.data)
        aspect.table = Table.query.get_or_404(table_id)
        db.session.add(aspect)
        db.session.commit()
        flash('Аспект был создан')
        return redirect(url_for('.get', table_id=table_id,
                                aspect_id=aspect.id))
    return render_template('aspects/create.html', form=form)


@aspects.route('/tables/<int:table_id>/aspects/<int:aspect_id>/update',
               methods=['GET', 'POST'])
def update(table_id, aspect_id):
    form = AspectForm()
    aspect = Aspect.query.get_or_404(aspect_id)
    if form.validate_on_submit():
        aspect.name = form.name.data
        db.session.commit()
        flash('Аспект был изменен')
        return redirect(url_for('.get', table_id=table_id,
                                aspect_id=aspect_id))
    form.name.data = aspect.name
    return render_template('aspects/update.html', form=form)


@aspects.route('/tables/<int:table_id>/aspects/<int:aspect_id>/delete',
               methods=['GET', 'POST'])
def delete(table_id, aspect_id):
    aspect = Aspect.query.get_or_404(aspect_id)
    db.session.delete(aspect)
    flash('Аспект был удален')
    return redirect(url_for('.get', table_id=table_id))