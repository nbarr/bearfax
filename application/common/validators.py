# -*- coding: utf-8 -*-

from wtforms.validators import ValidationError
from application.config.messages import get_message
from application.common.filters import strip_non_numeric


class BaseValidator(object):
    def __init__(self, readable_name=None, message=None):
        self.readable_name = readable_name
        self.message = message


class FaxRequired(BaseValidator):
    def __call__(self, form, field):
        try:
            if not strip_non_numeric(field.data):
                raise Exception()
        except:
            raise ValidationError(self.message or get_message('FAX_INVALID'))
