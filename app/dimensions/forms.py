# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class DimensionForm(Form):
    name = StringField('Имя', validators=[DataRequired()])
    aspect = SelectField('Аспект', coerce=int)
    submit = SubmitField('ok')