# -*- coding:utf-8 -*-
from itertools import product
from .. import db


class Matrix(db.Model):
    __tablename__ = 'matrix'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    levels = db.relationship('Level', backref='matrix', lazy='dynamic')
    aspects = db.relationship('Aspect', backref='matrix', lazy='dynamic')
    universums = db.relationship('Universum', backref='matrix', lazy='dynamic')
    dimensions = db.relationship('Dimension', backref='matrix', lazy='dynamic')

    def generate(self, level):
        if level in self.levels.all():
            raise Exception('{} already exist'.format(level))
        else:
            level.matrix = self
            db.session.add(level)
            db.session.commit()
            Aspect.generate(self, level)
            Universum.generate(self, level)

    def __repr__(self):
        return '<Matrix: {}>'.format(self.name)


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    aspects = db.relationship('Aspect', backref='level', lazy='dynamic')
    universums = db.relationship('Universum', backref='level', lazy='dynamic')

    @property
    def prev(self):
        return self.matrix.levels.filter_by(value=self.value-1).first()

    def __repr__(self):
        return '<Level: {}>'.format(self.value)


universum_aspect = db.Table('universum_aspect',
                            db.Column('universum_id', db.Integer, db.ForeignKey('universum.id')),
                            db.Column('aspect_id', db.Integer, db.ForeignKey('aspect.id')))

class Aspect(db.Model):
    __tablename__ = 'aspect'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
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
    def generate(matrix, level):
        superaspects = Aspect.query.filter_by(superaspect_id=None)
        if not superaspects:
            raise Exception('At least two aspects must be created')
        if level.prev:
            aspects_with_level = matrix.aspects.filter_by(level_id=level.prev.id).all()
        else:
            aspects_with_level = None
        base_aspects = aspects_with_level if aspects_with_level else superaspects
        for base_aspect, mixin_aspect in product(base_aspects, superaspects):
                aspect = Aspect()
                aspect.name = "{0}, {1}".format(mixin_aspect.name, base_aspect.name)
                aspect.matrix = matrix
                aspect.level = level
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
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    superuniversum_id = db.Column(db.Integer, db.ForeignKey(id))
    subuniversums = db.relationship('Universum',
                                    cascade='all, delete-orphan',
                                    backref=db.backref('superuniversum', remote_side=id))
    aspects = db.relationship('Aspect', secondary=universum_aspect,
                              backref=db.backref('universums', lazy='dynamic'))

    @staticmethod
    def generate(matrix, level):
        dimensions_aspects = (dimension.get_aspects(level) for dimension in matrix.dimensions)
        for aspects in product(*dimensions_aspects):
            universum = Universum()
            universum.name = '; '.join(reversed([aspect.name for aspect in aspects]))
            universum.matrix = matrix
            universum.level = level
            universum.aspects.extend(reversed(aspects))
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
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    aspect_id = db.Column(db.Integer, db.ForeignKey('aspect.id'))
    aspect = db.relationship('Aspect', uselist=False, backref='dimension')

    def get_aspects(self, level):
        return self.aspect.get_aspects(level)

    def __repr__(self):
        return '<Dimension: {}>'.format(self.name)