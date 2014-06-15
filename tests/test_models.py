# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.web.models import Table, Aspect, Universum, Dimension, Level


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

    def test_table_creation(self):
        # готовим данные
        table = Table(name='Мир')
        aspect_1 = Aspect(name='Неизменность')
        aspect_2 = Aspect(name='Единство')
        table.aspects.extend((aspect_1, aspect_2))
        db.session.add(table)
        db.session.commit()
        Aspect.generate(table)
        # получаем данные
        table = Table.query.get(table.id)
        # делаем проверки
        self.assertTrue(table.aspects[0].name == 'Неизменность')

    def test_aspect_creation(self):
        # готовим данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_1_1 = Aspect(name='Неизменность Неизменность', superaspect=aspect_1)
        db.session.add(aspect_1_1)
        db.session.commit()
        # получаем данные
        superaspect = Aspect.query.filter_by(name='Неизменность').first()
        subaspect = Aspect.query.filter_by(name='Неизменность Неизменность').first()
        # делаем проверки
        self.assertTrue(superaspect.name == 'Неизменность')
        self.assertTrue(superaspect.subaspects[0].name == 'Неизменность Неизменность')
        self.assertTrue(subaspect.superaspect.name == 'Неизменность')

    def test_universum_creation(self):
        # готовим данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        aspect_2 = Aspect(name='Единство')
        db.session.add(aspect_2)
        db.session.commit()
        superaspects = Aspect.query.filter(Aspect.superaspect_id == None)
        Aspect.generate(superaspects)
        Universum.generate(superaspects)
        # получаем данные
        aspect = Aspect.query.filter_by(name='Неизменность Единство').first()
        universum = Universum.query.filter_by(name='Неизменность Единство Неизменность Неизменность').first()
        # делаем проверки
        self.assertTrue(aspect.universums[0].name == 'Неизменность Единство Неизменность Неизменность')
        self.assertTrue(universum.aspects[0].name == 'Неизменность Единство')

    def test_dimension_creation(self):
        # готовим данные
        aspect_1 = Aspect(name='Неизменность')
        db.session.add(aspect_1)
        dimension_1 = Dimension(label='Форма', aspect=aspect_1)
        db.session.add(dimension_1)
        db.session.commit()
        # получаем данные
        dimension_1 = Dimension.query.filter(Dimension.label == 'Форма').first()
        # делаем проверки
        self.assertTrue(dimension_1.label == 'Форма')
        self.assertTrue(dimension_1.aspect.name == 'Неизменность')

    def test_level(self):
        # готовим данные
        level_1 = Level(value=1)
        aspect_1 = Aspect(name='Аспект 1-го уровня',
                          level=level_1)
        db.session.add(aspect_1)
        level_2 = Level(value=2)
        aspect_2 = Aspect(name='Аспект 2-го уровня',
                          superaspect=aspect_1,
                          level=level_2)
        db.session.add(aspect_2)
        level_3 = Level(value=3)
        aspect_3_1 = Aspect(name='Аспект 3-го уровня 1',
                          superaspect=aspect_2,
                          level=level_3)
        db.session.add(aspect_3_1)
        aspect_3_2 = Aspect(name='Аспект 3-го уровня 2',
                            superaspect=aspect_2,
                            level=level_3)
        db.session.add(aspect_3_2)
        db.session.commit()
        # получаем данные
        aspect_1 = Aspect.query.get(aspect_1.id)
        aspects = aspect_1.get_aspects(level_3)
        # делаем проверки
        self.assertTrue(aspects[0] is aspect_3_1)
        self.assertTrue(aspects[1] is aspect_3_2)
