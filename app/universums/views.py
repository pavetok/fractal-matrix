# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import universums
from .. import db
from ..models import Universum
from .forms import UniversumForm


@universums.route('/get', methods=['GET'])
def get():
    universums = Universum.query.all()
    return render_template('universums_get.html', universums=universums)

@universums.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    universum = Universum.query.get_or_404(id)
    return render_template('universums_get_by_id.html', universum=universum)

@universums.route('/add', methods=['GET', 'POST'])
def add():
    form = UniversumForm()
    if form.validate_on_submit():
        universum = Universum(name=form.name.data)
        db.session.add(universum)
        db.session.commit()
        flash('Универсум был добавлен')
        universum = Universum.query.filter_by(name=universum.name).first()
        return redirect(url_for('.get_by_id', id=universum.id))
    return render_template('universums_add.html', form=form)

@universums.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    universum = Universum.query.get_or_404(id)
    form = UniversumForm()
    if form.validate_on_submit():
        universum.name = form.name.data
        db.session.commit()
        flash('Универсум был изменен')
        return redirect(url_for('.get_by_id', id=universum.id))
    form.name.data = universum.name
    return render_template('universums_upd.html', form=form)

@universums.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    universum = Universum.query.get_or_404(id)
    db.session.delete(universum)
    flash('Универсум был удален')
    return redirect(url_for('.get'))