# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.models import Aspect, Universum, generate_aspects, generate_universums


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

    def test_universum_creation(self):
        # создаем данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Единство')
        db.session.add(aspect_2)
        db.session.commit()
        generate_aspects()
        generate_universums()
        # получаем данные
        aspect = Aspect.query.filter_by(name='Неизменность Неизменность').first()
        universum = Universum.query.filter_by(name='Единство Неизменность, Неизменность Неизменность').first()
        # делаем проверки
        self.assertTrue(aspect.universums[0].name == 'Единство Неизменность, Неизменность Неизменность')
        print(universum.aspects[0].name)
        self.assertTrue(universum.aspects[0].name == 'Единство Неизменность')

    def test_table_creation(self):
        # создаем данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Единство')
        db.session.add(aspect_2)
        db.session.commit()
        generate_aspects()
        # получаем данные
        aspects = Aspect.query.filter(Aspect.superaspect_id != None)
        # делаем проверки
        self.assertTrue(aspects[0].name == 'Неизменность Неизменность')