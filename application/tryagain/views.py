# -*- coding: utf-8 -*-

import uuid
from flask import abort, render_template, request
from flask.views import MethodView
from application.common.token_serialize import deserialize, serialize
from application.config.messages import get_message
from application.extensions import recaptcha
from application.models import Task
from application.database import session
from application.tryagain.forms import TryAgainForm
from application.common.mailer import send_confirmation_mail


class TryagainMethodView(MethodView):
    def get(self, token):
        expired, invalid, data = deserialize(token)

        if invalid:
            abort(404)

        try:
            task = session.query(Task).filter(Task.task_uid == data.get('task_uid', -1)).one()

            if not task or task.status != Task.STATUS_FAILED:
                abort(404)
        except:
            abort(404)

        form = TryAgainForm(obj=task)
        form.email.data = task.user.email

        return render_template('tryagain.html', form=form, token=token)

    def post(self, token):
        expired, invalid, data = deserialize(token)
        error = ''

        if invalid:
            abort(404)

        form = TryAgainForm()

        if form.validate_on_submit() and recaptcha.verify():
            try:
                task = session.query(Task).filter(Task.task_uid == data.get('task_uid', -1)).one()

                if not task:
                    abort(404)
            except:
                abort(404)

            if task.fax != form.fax.data:
                task.fax = form.fax.data
                task.status = Task.STATUS_UNCONFIRMED
                task.task_uid = uuid.uuid4().hex
                task.twilio_status = None
                session.commit()

                token = serialize({'user_id': task.user.id, 'task_id': task.id, 'task_uid': task.task_uid})
                send_confirmation_mail([task.user.email], task, token)
                return render_template('verify_email.html')

            form.fax.errors.append(get_message('FAX_MUST_BE_CHANGED'))
            form.document_orig_name.data = task.document_orig_name
            form.email.data = task.user.email

        if not request.form.get('g-recaptcha-response', '').strip():
            form.errors['g-recaptcha-response'] = [get_message('RECAPTCHA_REQUIRED')]

        return render_template('tryagain.html', form=form, token=token, error=error)
