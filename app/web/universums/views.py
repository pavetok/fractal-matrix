# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import universums
from ... import db
from ..models import Table, Aspect, Universum
from .forms import UniversumForm


@universums.route('/tables/<int:table_id>/universums/generate')
def generate(table_id):
    table = Table.query.get_or_404(table_id)
    Universum.generate(table)
    return redirect(url_for('.get', table_id=table_id))


@universums.route('/tables/<int:table_id>/universums')
@universums.route('/tables/<int:table_id>/universums/<int:universum_id>')
def get(table_id, universum_id=None):
    table = Table.query.get_or_404(table_id)
    if universum_id is None:
        return render_template('universums/get.html', table=table)
    else:
        universum = Universum.query.get_or_404(universum_id)
        return render_template('universums/get_by_id.html', table=table,
                               universum=universum)

@universums.route('/tables/<int:table_id>/universums/create',
                  methods=['GET', 'POST'])
def create(table_id):
    form = UniversumForm()
    if form.validate_on_submit():
        universum = Universum(name=form.name.data)
        universum.table = Table.query.get_or_404(table_id)
        db.session.add(universum)
        db.session.commit()
        flash('Универсум был создан')
        return redirect(url_for('.get', table_id=table_id,
                                universum_id=universum.id))
    return render_template('universums/create.html', form=form)

@universums.route('/tables/<int:table_id>/universums/<int:universum_id>/update',
                  methods=['GET', 'POST'])
def update(table_id, universum_id):
    form = UniversumForm()
    universum = Universum.query.get_or_404(universum_id)
    if form.validate_on_submit():
        universum.name = form.name.data
        db.session.commit()
        flash('Универсум был изменен')
        return redirect(url_for('.get', table_id=table_id,
                                universum_id=universum_id))
    form.name.data = universum.name
    return render_template('universums/update.html', form=form)

@universums.route('/tables/<int:table_id>/universums/<int:universum_id>/delete',
                  methods=['GET', 'POST'])
def delete(table_id, universum_id):
    universum = Universum.query.get_or_404(universum_id)
    db.session.delete(universum)
    flash('Универсум был удален')
    return redirect(url_for('.get', table_id=table_id))