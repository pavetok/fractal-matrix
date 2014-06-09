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
        self.app_context.pop()

    def test_aspect_creation(self):
        # готовим данные
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
        # готовим данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Единство')
        db.session.add(aspect_2)
        db.session.commit()
        superaspects = Aspect.query.filter(Aspect.superaspect_id == None)
        generate_aspects(superaspects)
        generate_universums(superaspects)
        # получаем данные
        aspect = Aspect.query.filter_by(name='Неизменность Единство').first()
        universum = Universum.query.filter_by(name='Неизменность Единство Неизменность Неизменность').first()
        # делаем проверки
        self.assertTrue(aspect.universums[0].name == 'Неизменность Единство Неизменность Неизменность')
        self.assertTrue(universum.aspects[0].name == 'Неизменность Единство')

    def test_table_creation(self):
        # готовим данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Единство')
        db.session.add(aspect_2)
        db.session.commit()
        superaspects = Aspect.query.filter(Aspect.superaspect_id == None)
        generate_aspects(superaspects)
        # получаем данные
        aspects = Aspect.query.filter(Aspect.superaspect_id != None)
        # делаем проверки
        self.assertTrue(aspects[0].name == 'Неизменность Неизменность')

    def test_level(self):
        # готовим данные
        aspect_1 = Aspect(name='Аспект 1-го уровня')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Аспект 2-го уровня', superaspect=aspect_1)
        db.session.add(aspect_2)
        aspect_3 = Aspect(name='Аспект 3-го уровня', superaspect=aspect_2)
        db.session.add(aspect_3)
        db.session.commit()
        # получаем данные
        aspect_1 = Aspect.query.filter(Aspect.name == 'Аспект 1-го уровня').first()
        aspect_2 = Aspect.query.filter(Aspect.name == 'Аспект 2-го уровня').first()
        aspect_3 = Aspect.query.filter(Aspect.name == 'Аспект 3-го уровня').first()
        # делаем проверки
        self.assertTrue(aspect_1.level == 1)
        self.assertTrue(aspect_2.level == 2)
        self.assertTrue(aspect_3.level == 3)
