# -*- coding: utf-8 -*-

from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask import current_app
from application.config import settings


def get_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


def serialize(data):
    return get_serializer().dumps(data)


def deserialize(token):
    expired, invalid, data = False, False, None

    serializer = get_serializer()

    try:
        data = serializer.loads(token, max_age=settings.S3_EXPIRATION_SECONDS)
    except SignatureExpired:
        _, data = serializer.loads_unsafe(token)
        expired = True
    except:
        invalid = True

    return expired, invalid, data
