# -*- coding: utf-8 -*-

import os

# Here stored settings related to Flask instance and extensions
# Normally this file should not be imported anywhere

SECRET_KEY = 'd+/6n~G@]gt.&j"%pku?5<7?GcP;?fDn-3)%cg~g&NN%3LmhH#fmW!A(\4a8Vr%ff4%ZHMk&(J(54q_'
ENV = os.getenv('ENVIRONMENT')
DEBUG = ENV != 'production'
LOGGER_NAME = 'flask'

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = '2d47a98bf26049cfae5656e2b244e8eb2d47a98bf26049cfae5656e2b244e8eb'

# Flask-Security

SECURITY_REGISTERABLE = False
SECURITY_CONFIRMABLE = False
SECURITY_RECOVERABLE = False
SECURITY_CHANGEABLE = False
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = '59)()2^9JPD&SFGq'

# Flask-Mail

MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS'))
MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL'))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

# Twilio

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE = os.getenv('TWILIO_PHONE')

# Amazon AWS

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY_ID = os.getenv('AWS_SECRET_KEY_ID')
AWS_BUCKET = os.getenv('AWS_BUCKET')

# Redis
REDIS_URI = os.getenv('REDIS_URI')

# Flask-Recaptcha
RECAPTCHA_ENABLED = bool(os.getenv('RECAPTCHA_ENABLED', True))
RECAPTCHA_SITE_KEY  = os.getenv('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY')
RECAPTCHA_THEME = os.getenv('RECAPTCHA_THEME')
RECAPTCHA_TYPE = os.getenv('RECAPTCHA_TYPE')
RECAPTCHA_SIZE = os.getenv('RECAPTCHA_SIZE')
RECAPTCHA_TABINDEX = -1
