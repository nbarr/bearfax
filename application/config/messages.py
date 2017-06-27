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
    'TASK_FAILED': ('Unable to send fax to the desired number <b>{fax}</b>, reason: <b>{reason}</b>. '
                     'You can click <a href="{url}">here and provide another fax number</a> then try again.'),
    'URL_EXPIRED': 'Your url is expired and cannot be used for confirmation anymore. Please try upload again.',
    'URL_INVALID': 'We cannot recognize token in your url, it is invalid.',
    'TASK_NOT_FOUND': 'Task not found.',
    'FAX_MUST_BE_CHANGED': 'Fax number cannot be the same as before and must be changed.',
    'MAX_PDF_PAGES_ALLOWED': 'Allowed maximum {pages} pages document, actual is {actual}.',
    'BAD_DATASET': 'Bad dataset: <b>{dataset}</b>',
    'QUEUE_FULL': 'Query is full, awating for available slot.',
    'SILL_SENDING': 'Fax sending is still in progresss.',
    'RECAPTCHA_REQUIRED': 'Recaptcha required.',
    'DOCUMENT_CONTAINS_VIRUSES': ('Your document <b>{document}</b> contain viruses and cannot be processed. '
                                  'Virus scan result: <b>{message}</b>.'),
    'INVALID_DOCUMENT': 'Document provided either is not a PDF or invalid.'
}

TWILIO_STATUSES = {
    'queued': 'Awaiting for processing',
    'processing': 'Processing and converting',
    'sending': 'Sending',
    'delivered': 'Delivered',
    'receiving': 'Receiving',
    'received': 'Received',
    'no-answer': 'No answer',
    'busy': 'Busy',
    'failed': 'Fax send failed on remote side',
    'canceled': 'Fax sending was cancelled'
}

TWILIO_ERROR_CODES = {
    21203: 'International calling not enabled'
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
