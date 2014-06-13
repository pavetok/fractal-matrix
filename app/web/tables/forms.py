# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TableForm(Form):
    name = StringField('Имя', validators=[DataRequired()])
    submit = SubmitField('ok')