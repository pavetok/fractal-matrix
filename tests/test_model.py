# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.models import Aspect, Universum


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_aspect_creation(self):
        aspect = Aspect(name='Неизменность')
        db.session.add(aspect)
        aspect = Aspect(name='Целостность')
        db.session.add(aspect)
        db.session.commit()
        aspects = Aspect.query.all()
        self.assertTrue(aspects[0].name == 'Неизменность')
        self.assertTrue(aspects[1].name == 'Целостность')

    def test_universum_creation(self):
        universum = Universum(name='Неизменность')
        db.session.add(universum)
        universum = Universum(name='Целостность')
        db.session.add(universum)
        db.session.commit()
        universums = Universum.query.all()
        self.assertTrue(universums[0].name == 'Неизменность')
        self.assertTrue(universums[1].name == 'Целостность')