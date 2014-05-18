# -*- coding:utf-8 -*-
from . import db


class Ипостась(db.Model):
    __tablename__ = 'essences'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Ипостась: {}>'.format(self.name)