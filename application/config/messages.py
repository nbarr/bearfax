# -*- coding: utf-8 -*-


FIELDS = {
    'EMAIL': {
        'label': 'Email',
        'description': 'Email field used as login',
        'placeholder': 'E-Mail'
    }
}

MESSAGES = {
    'UNKNOWN_ERROR': 'Unknown error occures. Please reload page and try again.',
    'NO_SUCH_USER': 'No users found accordingly to your criteria.',
    'USER_NOT_AUTHORIZED': 'User is not authorised to perform this action.',
    'USER_NOT_AUTHENTICATED': 'User is not authenticated.',

    'NOT_FOUND': 'Resource not found.',
    'FAX_INVALID': 'Fax number is invalid.',
    'TASK_UNCONFIRMED': 'Your request was not confirmed, please check your email and click on link in it.',
    'TASK_FAILED': ('Fax number you provided does not answer either not available so your fax cannot be sent there. '
                     'You can click <a href="{url}">here and provide another fax number</a> then try again.'),
    'URL_EXPIRED': 'Your url is expired and cannot be used for confirmation anymore. Please try upload again.',
    'URL_INVALID': 'We cannot recognize token in your url, it is invalid.',
    'TASK_NOT_FOUND': 'Task not found.',
    'FAX_MUST_BE_CHANGED': 'Fax number cannot be the same as before and must be changed.'
}


def _safe_format(template, **kwargs):
    context = dict((key, value) for key, value in kwargs.items() if '{{{k}}}'.format(k=key) in template)
    return template.format(**context)


def get_message(key, source=MESSAGES, **kwargs):
    template = source.get(key, None)
    return key if not template else _safe_format(template, **kwargs)


def get_field_label(key, source=FIELDS, required=False, **kwargs):
    template = source.get(key, {}).get('label')

    if not template:
        return key

    value = _safe_format(template, **kwargs)

    if required:
        value += ' *'

    return value


def get_field_placeholder(key, source=FIELDS, **kwargs):
    template = source.get(key, {}).get('placeholder')
    return key if not template else _safe_format(template, **kwargs)


def get_field_description(key, source=FIELDS, **kwargs):
    template = source.get(key, {}).get('description')
    return key if not template else _safe_format(template, **kwargs)
