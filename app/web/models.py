# -*- coding:utf-8 -*-
from .. import db


table_level = db.Table('table_level',
                       db.Column('table_id', db.Integer, db.ForeignKey('table.id')),
                       db.Column('level_id', db.Integer, db.ForeignKey('level.id')))

class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    levels = db.relationship('Level', secondary=table_level,
                             backref=db.backref('tables', lazy='dynamic'))
    aspects = db.relationship('Aspect', backref='table', lazy='dynamic')
    universums = db.relationship('Universum', backref='table', lazy='dynamic')
    dimensions = db.relationship('Dimension', backref='table', lazy='dynamic')
    # hypostases = None

    def __repr__(self):
        return '<Table: {}>'.format(self.name)


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64), unique=True)
    aspects = db.relationship('Aspect', backref='level', lazy='dynamic')
    universums = db.relationship('Universum', backref='level', lazy='dynamic')

    def __repr__(self):
        return '<Level: {}>'.format(self.name)


universum_aspect = db.Table('universum_aspect',
                            db.Column('universum_id', db.Integer, db.ForeignKey('universum.id')),
                            db.Column('aspect_id', db.Integer, db.ForeignKey('aspect.id')))

class Aspect(db.Model):
    __tablename__ = 'aspect'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    superaspect_id = db.Column(db.Integer, db.ForeignKey(id))
    subaspects = db.relationship('Aspect',
                                 cascade='all, delete-orphan',
                                 backref=db.backref('superaspect', remote_side=id))

    @staticmethod
    def generate(table):
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        for primary_aspect in superaspects:
            for mixin_aspect in superaspects:
                subaspect = Aspect(name="{0} {1}".format(mixin_aspect.name,
                                                         primary_aspect.name))
                subaspect.table = table
                subaspect.superaspect = primary_aspect
                db.session.add(subaspect)
        db.session.commit()

    @staticmethod
    def update_dependent(superaspect, new_name, old_name, initiator):
        for aspect in superaspect.subaspects:
            if old_name in aspect.name:
                aspect.name = aspect.name.replace(old_name, new_name)
                db.session.add(aspect)
        for universum in superaspect.universums:
            if old_name in universum.name:
                universum.name = universum.name.replace(old_name, new_name)
                db.session.add(universum)
        db.session.commit()

    def __repr__(self):
        return '<Aspect: {}>'.format(self.name)
# события
db.event.listen(Aspect.name, 'set', Aspect.update_dependent)


class Universum(db.Model):
    __tablename__ = 'universum'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    superuniversum_id = db.Column(db.Integer, db.ForeignKey(id))
    subuniversums = db.relationship('Universum',
                                    cascade='all, delete-orphan',
                                    backref=db.backref('superuniversum', remote_side=id))
    aspects = db.relationship('Aspect', secondary=universum_aspect,
                              backref=db.backref('universums', lazy='dynamic'))

    @staticmethod
    def generate(table):
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        if len(list(superaspects)) == 2:
            (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
            for x_aspect in x_aspects:
                for y_aspect in y_aspects:
                    universum = Universum(name="{0} {1}".format(y_aspect.name,
                                                                x_aspect.name))
                    universum.table = table
                    universum.aspects = [y_aspect, x_aspect]
                    db.session.add(universum)
            db.session.commit()

    @staticmethod
    def update_dependent(superuniversum, new_name, old_name, initiator):
        for universum in superuniversum.subuniversums:
            if old_name in universum.name:
                universum.name = universum.name.replace(old_name, new_name)
                db.session.add(universum)
        db.session.commit()

    def __repr__(self):
        return '<Universum: {}>'.format(self.name)
# события
db.event.listen(Universum.name, 'set', Universum.update_dependent)


class Dimension(db.Model):
    __tablename__ = 'dimension'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    aspect_id = db.Column(db.Integer, db.ForeignKey('aspect.id'))
    aspect = db.relationship('Aspect', uselist=False, backref='dimension')

    def __repr__(self):
        return '<Dimension: {}>'.format(self.name)