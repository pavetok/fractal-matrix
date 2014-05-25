# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class UniversumForm(Form):
    name = StringField('Имя', validators=[Required()])
    submit = SubmitField('ok')