# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, redirect, url_for
from flask.views import MethodView
from application.common.token_serialize import deserialize
from application.config.messages import get_message
from application.models import Task
from application.database import session


class ProcessMethodView(MethodView):
    def get(self, token):
        expired, invalid, data = deserialize(token)

        if invalid:
            return render_template('process.html', error_message=get_message('URL_INVALID'))

        try:
            task = session.query(Task).filter(Task.task_uid == data.get('task_uid', -1)).one()
        except:
            return render_template('process.html', error_message=get_message('TASK_NOT_FOUND'))

        if not task:
            return render_template('process.html', error_message=get_message('TASK_NOT_FOUND'))

        if expired and task.status == Task.STATUS_UNCONFIRMED:
            return render_template('process.html', error_message=get_message('URL_EXPIRED'))

        if task.status in [Task.STATUS_SENT]:
            return redirect(url_for('views.home'))

        if task.user:
            if not task.user.confirmed_at:
                task.user.confirmed_at = datetime.utcnow()
                task.user.active = True

        if task.status == Task.STATUS_UNCONFIRMED:
            task.status = Task.STATUS_PENDING

        session.commit()

        return render_template('process.html')

        # return render_template('process.html', error_message='''This is temporary message indicated that
        # your document was uploaded and ready for prcessing. It will expires (and automatically removed) in
        # <b>{}</b> days. Public URL of your pdf is <b>{}</b>.
        # '''.format(settings.S3_EXPIRATION_DAYS, task.url))
