# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import universums
from .. import db
from ..models import Universum
from .app.tables.universums.forms import UniversumForm


@universums.route('')
@universums.route('/<int:id>')
def get(id=None):
    if id is None:
        universums = Universum.query.all()
        return render_template('universums_get.html', universums=universums)
    else:
        universum = Universum.query.get_or_404(id)
        return render_template('universums_get_by_id.html', universum=universum)

@universums.route('/create', methods=['GET', 'POST'])
def create():
    form = UniversumForm()
    if form.validate_on_submit():
        universum = Universum(name=form.name.data)
        db.session.add(universum)
        db.session.commit()
        flash('Универсум был создан')
        universum = Universum.query.filter_by(name=universum.name).first()
        return redirect(url_for('.get', id=universum.id))
    return render_template('universums_create.html', form=form)

@universums.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    universum = Universum.query.get_or_404(id)
    form = UniversumForm()
    if form.validate_on_submit():
        universum.name = form.name.data
        db.session.commit()
        flash('Универсум был изменен')
        return redirect(url_for('.get', id=universum.id))
    form.name.data = universum.name
    return render_template('universums_update.html', form=form)

@universums.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    universum = Universum.query.get_or_404(id)
    db.session.delete(universum)
    flash('Универсум был удален')
    return redirect(url_for('.get'))