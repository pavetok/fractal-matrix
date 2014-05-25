# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class AspectForm(Form):
    name = StringField('Имя аспекта', validators=[Required()])
    submit = SubmitField('ok')

class AspectAddForm(Form):
    name = StringField('Имя аспекта', validators=[Required()])
    submit = SubmitField('ok')

class AspectUpdForm(Form):
    name = StringField('Имя аспекта', validators=[Required()])
    submit = SubmitField('ok')