# -*- coding:utf-8 -*-
from flask import render_template, url_for, flash, redirect
from . import core
from .. import db
from ..models import Aspect, Universum, generate_aspects, generate_universums
from .forms import AspectForm, AspectAddForm, AspectUpdForm


@core.route('/gena')
def gena():
    generate_aspects()
    return redirect(url_for('.index'))

@core.route('/genu')
def genu():
    generate_universums()
    return redirect(url_for('.index'))

@core.route('/')
def index():
    universums = Universum.query.all()
    first_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 0)
    second_row_of_universums = (universum for universum in universums if \
                    universums.index(universum) % 2 == 1)
    superaspects = Aspect.query.filter_by(superaspect_id=None)
    if len(list(superaspects)) == 2:
        (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
        return render_template('index.html',
                               x_aspects=reversed(x_aspects),
                               y_aspects=y_aspects,
                               first_row_of_universums=first_row_of_universums,
                               second_row_of_universums=second_row_of_universums)
    else:
        return render_template('index.html')

@core.route('/aspects', methods=['GET'])
def aspects_get():
    aspects = Aspect.query.all()
    return render_template('aspects_get.html', aspects=aspects)

@core.route('/aspects/<int:id>', methods=['GET'])
def aspects_get_by_id(id):
    aspect = Aspect.query.get_or_404(id)
    return render_template('aspects_get_by_id.html', aspect=aspect)

@core.route('/aspects', methods=['POST'])
def aspects_add():
    form = AspectForm()
    if form.validate_on_submit():
        aspect = Aspect(name=form.name.data)
        db.session.add(aspect)
        flash('Аспект был добавлен')
        return redirect(url_for('.aspects', id=aspect.id))
    return render_template('aspect_add.html', form=form)

@core.route('/aspects/<int:id>', methods=['PUT'])
def aspects_upd(id):
    aspect = Aspect.query.get_or_404(id)
    form = AspectForm()
    if form.validate_on_submit():
        aspect.name = form.name.data
        db.session.add(aspect)
        flash('Аспект был изменен')
        return redirect(url_for('.aspects', id=aspect.id))
    form.name.data = aspect.name
    return render_template('aspects_upd.html', form=form)

@core.route('/aspects/<int:id>', methods=['DELETE'])
def aspects_del(id):
    aspect = Aspect.query.get_or_404(id)
    db.session.delete(aspect)
    flash('Аспект был удален')
    return redirect(url_for('.aspects'))