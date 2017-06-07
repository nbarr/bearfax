# -*- coding: utf-8 -*-

from flask import render_template
from flask.views import MethodView
from application.common.token_serialize import deserialize
from application.config.messages import get_message
from application.config import settings
from application.models import Task
from application.database import session


class ProcessMethodView(MethodView):
    def get(self, token):
        expired, invalid, data = deserialize(token)

        if expired:
            return render_template('process.html', error_message=get_message('URL_EXPIRED'))

        if invalid:
            return render_template('process.html', error_message=get_message('URL_INVALID'))

        task = session.query(Task).get(data['task_id'])

        if not task:
            return render_template('process.html', error_message=get_message('TASK_NOT_FOUND'))

        return render_template('process.html', error_message='''This is temporary message indicated that
        your document was uploaded and reay for prcessing. It will expires (and automatically removed) in
        <b>{}</b> days. Public URL of your pdf is <b>{}</b>.
        '''.format(settings.S3_EXPIRATION_DAYS, task.url))
