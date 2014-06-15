# -*- coding:utf-8 -*-
from .. import db


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    levels = db.relationship('Level', backref='table', lazy='dynamic')
    aspects = db.relationship('Aspect', backref='table', lazy='dynamic')
    universums = db.relationship('Universum', backref='table', lazy='dynamic')
    dimensions = db.relationship('Dimension', backref='table', lazy='dynamic')

    def generate(self, level):
        if level not in self.levels:
            Aspect.generate(self, level)
            Universum.generate(self, level)

    def __repr__(self):
        return '<Table: {}>'.format(self.name)


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    aspects = db.relationship('Aspect', backref='level', lazy='dynamic')
    universums = db.relationship('Universum', backref='level', lazy='dynamic')

    def __repr__(self):
        return '<Level: {}>'.format(self.value)


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

    def get_aspects(self, level):
        aspects_with_level = []
        for aspect in self.subaspects:
            if aspect.level is level:
                aspects_with_level.append(aspect)
        if aspects_with_level:
            return aspects_with_level
        for aspect in self.subaspects:
            aspects_with_level.extend(aspect.get_aspects(level))
        return aspects_with_level

    @staticmethod
    def generate(table, level=None):
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        if not level:
            base_aspects = superaspects
        else:
            base_aspects = Table.aspects.filter_by(level_id=level.id)
        for base_aspect in base_aspects:
            for mixin_aspect in superaspects:
                aspect = Aspect(name="{0}; {1}".format(mixin_aspect.name,
                                                       base_aspect.name))
                aspect.table = table
                aspect.superaspect = base_aspect
                db.session.add(aspect)
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
    def generate(table, level=None):
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        superaspects = Aspect.query.filter_by(level_id=level.id)
        (x_aspects, y_aspects) = (superaspect.subaspects for superaspect in superaspects)
        for x_aspect in x_aspects:
            for y_aspect in y_aspects:
                universum = Universum(name="{0}; {1}".format(y_aspect.name,
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

    def get_aspects(self, level):
        return self.aspect.get_aspects(level)

    def __repr__(self):
        return '<Dimension: {}>'.format(self.name)