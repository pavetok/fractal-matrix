# -*- coding:utf-8 -*-
import unittest
from app import create_app, db
from app.web.models import Matrix, Aspect, Universum, Dimension, Level


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

    def test_matrix_generation(self):
        matrix = matrix_create(2)
        # делаем проверки
        self.assertTrue(matrix.aspects.filter_by(name='Единство, Неизменность').first())
        self.assertTrue(matrix.universums.filter_by(
            name='Единство, Изменчивость; Единство, Неизменность; Единство, Единство').first())

    def test_levels(self):
        # готовим данные
        matrix = Matrix(name='Мир')
        level_1 = Level(value=1, matrix=matrix)
        aspect_1 = Aspect(name='Аспект 1-го уровня', level=level_1)
        db.session.add(aspect_1)
        level_2 = Level(value=2, matrix=matrix)
        aspect_2_1 = Aspect(name='Аспект 2-го уровня 1', superaspect=aspect_1, level=level_2)
        db.session.add(aspect_2_1)
        aspect_2_2 = Aspect(name='Аспект 2-го уровня 2', superaspect=aspect_1, level=level_2)
        db.session.add(aspect_2_2)
        level_3 = Level(value=3, matrix=matrix)
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


def matrix_create(max_level):
    matrix = Matrix(name='Мир')
    level = Level(value=1, matrix=matrix)
    universum = Universum(name='Мир', level=level)
    matrix.universums.append(universum)
    aspect_1 = Aspect(name='Единство', level=level)
    aspect_1.universums.append(universum)
    matrix.aspects.append(aspect_1)
    aspect_2 = Aspect(name='Неизменность', level=level)
    aspect_2.universums.append(universum)
    matrix.aspects.append(aspect_2)
    aspect_3 = Aspect(name='Изменчивость', level=level)
    aspect_3.universums.append(universum)
    matrix.aspects.append(aspect_3)
    dimension_1 = Dimension(name='Типы', type='x', aspect=aspect_1)
    matrix.dimensions.append(dimension_1)
    dimension_2 = Dimension(name='Формы', type='y', aspect=aspect_2)
    matrix.dimensions.append(dimension_2)
    dimension_3 = Dimension(name='Объекты', type='z', aspect=aspect_3)
    matrix.dimensions.append(dimension_3)
    db.session.add(matrix)
    db.session.commit()
    for level_value in range(2, max_level + 1):
        new_level = Level(value=level_value, matrix=matrix)
        matrix.generate(new_level)
    return matrix


