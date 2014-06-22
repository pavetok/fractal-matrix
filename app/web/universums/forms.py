# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired


class UniversumSimpleForm(Form):
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('ok')

class UniversumFullForm(Form):
    name = StringField('Имя', validators=[DataRequired()])
    level = SelectField('Уровень', coerce=int)
    aspects = SelectMultipleField('Аспекты', coerce=int)
    submit = SubmitField('ok')