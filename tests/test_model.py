# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.models import Ипостась


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

    def test_создание_ипостаси(self):
        ипостась = Ипостась(name='Неизменность')
        db.session.add(ипостась)
        ипостась = Ипостась(name='Целостность')
        db.session.add(ипостась)
        db.session.commit()
        ипостаси = Ипостась.query.all()
        self.assertTrue(ипостаси[0].name == 'Неизменность')
        self.assertTrue(ипостаси[1].name == 'Целостность')