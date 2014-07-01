# -*- coding:utf-8 -*-
from itertools import product
from .. import db


class Matrix(db.Model):
    __tablename__ = 'matrix'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    levels = db.relationship('Level', backref='matrix', lazy='dynamic',
                             cascade='all, delete-orphan')
    aspects = db.relationship('Aspect', backref='matrix', lazy='dynamic',
                              cascade='all, delete-orphan')
    universums = db.relationship('Universum', backref='matrix', lazy='dynamic',
                                 cascade='all, delete-orphan')
    dimensions = db.relationship('Dimension', backref='matrix', lazy='dynamic',
                                 cascade='all, delete-orphan')

    def get_slice(self, level, universum):
        x_dimension = self.dimensions.filter_by(type='x').first()
        x_aspects = x_dimension.get_aspects(level)
        y_dimension = self.dimensions.filter_by(type='y').first()
        y_aspects = y_dimension.get_aspects(level)
        z_dimension = self.dimensions.filter_by(type='z').first()
        z_aspects = z_dimension.get_aspects(level) if z_dimension else None
        rows = list()
        for y_aspect in reversed(y_aspects):
            row = list()
            row.append(y_aspect)
            if len(list(self.dimensions)) == 2:
                row.extend(reversed(list(y_aspect.universums)))
            elif len(list(self.dimensions)) == 3:
                for x_aspect, z_aspect in zip(x_aspects, z_aspects):
                    universum_for_row = universum.subuniversums.filter(
                        Universum.aspects.contains(x_aspect),
                        Universum.aspects.contains(y_aspect),
                        Universum.aspects.contains(z_aspect)).first() or \
                                        y_aspect.universums.filter(
                        Universum.aspects.contains(x_aspect),
                        Universum.aspects.contains(y_aspect),
                        Universum.aspects.contains(z_aspect)).first() or \
                                        universum
                    row.append(universum_for_row)
            rows.append(row)
        # добавляем заголовки столбцов матрицы
        last_row_aspects = list()
        last_row_aspects.append('')  # пустая ячейка
        last_row_aspects.extend(x_aspects)
        rows.append(last_row_aspects)
        return rows

    def generate(self, level):
        if self.is_level(level):
            raise Exception('{} already exist'.format(level))
        else:
            Aspect.generate(self, level)
            Universum.generate(self, level)

    def is_level(self, level):
        return level.value in (level.value for level in self.levels)

    def __repr__(self):
        return '<Matrix: {}>'.format(self.name)


class Level(db.Model):
    __tablename__ = 'level'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    aspects = db.relationship('Aspect', backref='level', lazy='dynamic',
                              cascade='all, delete-orphan')
    universums = db.relationship('Universum', backref='level', lazy='dynamic',
                                 cascade='all, delete-orphan')

    def __init__(self, value, matrix):
        self.value = value
        self.matrix = matrix

    @property
    def prev(self):
        return self.matrix.levels.filter_by(value=self.value - 1).first()

    @property
    def next(self):
        return self.matrix.levels.filter_by(value=self.value + 1).first()

    def __repr__(self):
        return '<Level: {}>'.format(self.value)


universum_aspect = db.Table('universum_aspect',
                            db.Column('universum_id', db.Integer, db.ForeignKey('universum.id')),
                            db.Column('aspect_id', db.Integer, db.ForeignKey('aspect.id')))

class Aspect(db.Model):
    __tablename__ = 'aspect'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    superaspect_id = db.Column(db.Integer, db.ForeignKey(id))
    subaspects = db.relationship('Aspect',
                                 cascade='all, delete-orphan',
                                 lazy='dynamic',
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
        if len(list(superaspects)) < 2:
            raise Exception('At least two superaspects must be created')
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
        return '<Aspect #{0}: {1}>'.format(self.id, self.name)
# события
db.event.listen(Aspect.name, 'set', Aspect.update_dependent)


class Universum(db.Model):
    __tablename__ = 'universum'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), unique=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    superuniversum_id = db.Column(db.Integer, db.ForeignKey(id))
    subuniversums = db.relationship('Universum',
                                    lazy='dynamic',
                                    cascade='all, delete-orphan',
                                    backref=db.backref('superuniversum', remote_side=id))
    aspects = db.relationship('Aspect',
                              lazy='dynamic',
                              secondary=universum_aspect,
                              backref=db.backref('universums', lazy='dynamic'))

    @staticmethod
    def generate(matrix, level):
        if level.prev:
            superuniversums = matrix.universums.filter_by(level_id=level.prev.id)
        else:
            raise Exception('Should be at least one superuniversum')
        for superuniversum in superuniversums:
            subaspects = (aspect.subaspects \
                          for aspect in superuniversum.aspects.order_by('id'))
            for aspects in product(*subaspects):
                universum = Universum()
                universum.name = '; '.join(aspect.name for aspect in aspects)
                universum.matrix = matrix
                universum.level = level
                universum.superuniversum = superuniversum
                universum.aspects.extend(aspects)
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
        return '<Universum #{0}: {1}>'.format(self.id, self.name)
# события
db.event.listen(Universum.name, 'set', Universum.update_dependent)


class Dimension(db.Model):
    __tablename__ = 'dimension'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    type = db.Column(db.String(1), unique=True)
    matrix_id = db.Column(db.Integer, db.ForeignKey('matrix.id'))
    aspect_id = db.Column(db.Integer, db.ForeignKey('aspect.id'))
    aspect = db.relationship('Aspect', uselist=False, backref='dimension')

    def get_aspects(self, level):
        return self.aspect.get_aspects(level) or [self.aspect]

    def __repr__(self):
        return '<Dimension: {}>'.format(self.name)