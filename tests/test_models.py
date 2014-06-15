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

    def test_table_generation(self):
        # готовим данные
        table = Table(name='Мир')
        aspect_1 = Aspect(name='Единство')
        aspect_2 = Aspect(name='Неизменность')
        table.aspects.extend((aspect_1, aspect_2))
        dimension_1 = Dimension(name='Типы', aspect=aspect_1)
        dimension_2 = Dimension(name='Формы', aspect=aspect_2)
        table.dimensions.extend((dimension_1, dimension_2))
        db.session.add(table)
        db.session.commit()
        # получаем данные
        table = Table.query.get(table.id)
        table.generate(Level(value=1))
        # делаем проверки
        self.assertTrue(table.aspects.filter_by(name='Единство, Неизменность').first())
        self.assertTrue(table.universums.filter_by(name='Единство, Неизменность; Единство, Единство').first())

    def test_levels(self):
        # готовим данные
        level_1 = Level(value=1)
        aspect_1 = Aspect(name='Аспект 1-го уровня', level=level_1)
        db.session.add(aspect_1)
        level_2 = Level(value=2)
        aspect_2_1 = Aspect(name='Аспект 2-го уровня 1', superaspect=aspect_1, level=level_2)
        db.session.add(aspect_2_1)
        aspect_2_2 = Aspect(name='Аспект 2-го уровня 2', superaspect=aspect_1, level=level_2)
        db.session.add(aspect_2_2)
        level_3 = Level(value=3)
        aspect_3_1 = Aspect(name='Аспект 3-го уровня 1', superaspect=aspect_2_1, level=level_3)
        db.session.add(aspect_3_1)
        aspect_3_2 = Aspect(name='Аспект 3-го уровня 2', superaspect=aspect_2_2, level=level_3)
        db.session.add(aspect_3_2)
        db.session.commit()
        # получаем данные
        aspect_1 = Aspect.query.get(aspect_1.id)
        aspects = aspect_1.get_aspects(level_3)
        # делаем проверки
        self.assertTrue(aspects[0] is aspect_3_1)
        self.assertTrue(aspects[1] is aspect_3_2)
