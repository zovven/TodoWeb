# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask_wtf import Form, RecaptchaField
from wtforms import HiddenField, BooleanField, StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange


class ProjectAddForm(Form):
    type = IntegerField("Project type", validators=[Length(min=0, max=5)])

    name = StringField("Project name", validators=[DataRequired(), Length(min=1, max=30)])

    p_all = IntegerField("Project length", validators=[DataRequired(), NumberRange(min=10, max=9999)])

    p_day = IntegerField("Project day", validators=[DataRequired(), NumberRange(min=3, max=999)])
