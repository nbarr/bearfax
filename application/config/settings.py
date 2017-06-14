# -*- coding: utf-8 -*-

# Here stored settings related application configuration and aimed to be imported

DATE_FORMAT = '%Y-%m-%d'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

S3_EXPIRATION_DAYS = 10
S3_EXPIRATION_SECONDS = 10 * 24 * 60 * 60

FAX_CONFIRMATION_EXPIRATION_SECONDS = 3 * 60 * 60   # Fax request must be confirmed in 3 hours

TWILIO_QUEUE_CAPACITY = 10

MAX_PDF_PAGES = 10

TWILIO_STATUSES_OK = ['delivered']
TWILIO_STATUSES_FAILED = ['no-answer', 'busy', 'failed', 'canceled']
