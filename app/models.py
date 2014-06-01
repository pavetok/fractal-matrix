# -*- coding:utf-8 -*-
from . import db


def generate_aspects(superaspects):
    for primary_aspect in superaspects:
        for mixin_aspect in superaspects:
            subaspect = Aspect(name="{0} {1}".format(mixin_aspect.name, primary_aspect.name),
                               superaspect=primary_aspect)
            db.session.add(subaspect)
    db.session.commit()

def generate_universums(superaspects):
    if len(list(superaspects)) == 2:
        (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
        for x_aspect in x_aspects:
            for y_aspect in y_aspects:
                universum = Universum(name="{0} {1}".format(y_aspect.name, x_aspect.name),
                                      aspects=[y_aspect, x_aspect])
                db.session.add(universum)
        db.session.commit()

universum_aspect = db.Table('universum_aspect',
                   db.Column('universum_id', db.Integer, db.ForeignKey('universum.id')),
                   db.Column('aspect_id', db.Integer, db.ForeignKey('aspect.id'))
)

class Aspect(db.Model):
    __tablename__ = 'aspect'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    superaspect_id = db.Column(db.Integer, db.ForeignKey(id))
    subaspects = db.relationship('Aspect',
                                 cascade='all, delete-orphan',
                                 backref=db.backref('superaspect', remote_side=id))

    def __repr__(self):
        return '<Aspect: {}>'.format(self.name)

class Universum(db.Model):
    __tablename__ = 'universum'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    superuniversum_id = db.Column(db.Integer, db.ForeignKey(id))
    subuniversums = db.relationship('Universum',
                                    cascade='all, delete-orphan',
                                    backref=db.backref('superuniversum', remote_side=id))
    aspects = db.relationship('Aspect', secondary=universum_aspect,
                              backref=db.backref('universums', lazy='dynamic'))

    def __repr__(self):
        return '<Universum: {}>'.format(self.name)