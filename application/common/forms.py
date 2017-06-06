# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField


class BaseForm(FlaskForm):
    submit = SubmitField()
