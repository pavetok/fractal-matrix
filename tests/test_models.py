# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.models import Aspect, Universum, generate_matrix


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def test_aspect_creation(self):
        # создаем данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_1_1 = Aspect(name='Неизменная Неизменность', superaspect=aspect_1)
        db.session.add(aspect_1_1)
        db.session.commit()
        # получаем данные
        superaspect = Aspect.query.filter_by(name='Неизменность').first()
        subaspect = Aspect.query.filter_by(name='Неизменная Неизменность').first()
        # делаем проверки
        self.assertTrue(superaspect.name == 'Неизменность')
        self.assertTrue(superaspect.subaspects[0].name == 'Неизменная Неизменность')
        self.assertTrue(subaspect.superaspect.name == 'Неизменность')

    def test_table_creation(self):
        # создаем данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Единство')
        db.session.add(aspect_2)
        db.session.commit()
        # создаем матрицу
        generate_matrix()
        # получаем данные
        aspects = Aspect.query.filter(Aspect.subaspect_id != None)
        # делаем проверки
        self.assertTrue(aspects[0].name == 'Неизменность Неизменность')

    def test_universum_creation(self):
        universum = Universum(name='Неизменность')
        db.session.add(universum)
        universum = Universum(name='Целостность')
        db.session.add(universum)
        db.session.commit()
        universums = Universum.query.all()
        self.assertTrue(universums[0].name == 'Неизменность')
        self.assertTrue(universums[1].name == 'Целостность')