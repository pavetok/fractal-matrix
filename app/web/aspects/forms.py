# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired


class AspectSimpleForm(Form):
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('ok')

class AspectFullForm(Form):
    name = StringField('Имя', validators=[DataRequired()])
    level = SelectField('Уровень', coerce=int)
    universums = SelectMultipleField('Универсумы', coerce=int)
    submit = SubmitField('ok')