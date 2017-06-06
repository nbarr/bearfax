# -*- coding: utf-8 -*-

from wtforms.fields import StringField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, Email

from application.common.forms import BaseForm


class HomeUploadForm(BaseForm):
    document = FileField('PDF File', validators=[FileRequired()], render_kw={
        'placeholder': 'Upload PDF file',
        'required': True
    })

    fax = StringField('Fax', validators=[Required()], render_kw={
        'placeholder': 'Fax',
        'required': True,
        'pattern': '[0-9+\(\)\-]+'
    })

    email = EmailField('Email', validators=[Required(), Email()], render_kw={
        'placeholder': 'Email',
        'required': True,
        'pattern': '.{2,}@.{2,}\..{2,}'
    })
    tos_accepted = BooleanField('ToS', validators=[Required()], render_kw={
        'required': True
    })

    submit = SubmitField()
