# -*- coding:utf-8 -*-
from . import db


class Aspect(db.Model):
    __tablename__ = 'aspects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    subaspect_id = db.Column(db.Integer, db.ForeignKey('aspects.id'))
    subaspects = db.relationship('Aspect',
                              cascade='all, delete-orphan',
                              backref=db.backref('superaspect', remote_side=id))

    def __repr__(self):
        return '<Aspect: {}>'.format(self.name)


class Universum(db.Model):
    __tablename__ = 'universums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # todo: реализовать аггрегацию аспектов
    # todo: реализовать композицию универсумов

    def __repr__(self):
        return '<Universum: {}>'.format(self.name)