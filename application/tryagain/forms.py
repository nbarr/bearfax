# -*- coding: utf-8 -*-

from wtforms.fields import StringField
from wtforms.validators import Required

from application.common.forms import BaseForm
from application.common.validators import FaxRequired


class TryAgainForm(BaseForm):
    fax = StringField('Fax', validators=[
        Required(),
        FaxRequired()
    ], render_kw={
        'placeholder': 'Fax',
        'required': True,
        'pattern': '[0-9+\(\)\-]+'
    })

    document_orig_name = StringField(render_kw={'disabled': True})

    email = StringField(render_kw={'disabled': True})
