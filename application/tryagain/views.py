# -*- coding: utf-8 -*-

from flask import abort, render_template
from flask.views import MethodView
from application.common.token_serialize import deserialize, serialize
from application.config.messages import get_message
from application.models import Task
from application.database import session
from application.tryagain.forms import TryAgainForm
from application.common.mailer import send_confirmation_mail


class TryagainMethodView(MethodView):
    def get(self, token):
        expired, invalid, data = deserialize(token)

        if invalid:
            abort(404)

        task = session.query(Task).get(data['task_id'])

        if not task or not task.status == Task.STATUS_FAILED:
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

        if form.validate_on_submit():
            task = session.query(Task).get(data['task_id'])

            if not task:
                abort(404)

            if task.fax != form.fax.data:
                task.fax = form.fax.data
                task.status = Task.STATUS_UNCONFIRMED
                session.commit()

                token = serialize({'user_id': task.user.id, 'task_id': task.id})
                send_confirmation_mail([task.user.email], task, token)
                return render_template('verify_email.html')

            form.fax.errors.append(get_message('FAX_MUST_BE_CHANGED'))
            form.document_orig_name.data = task.document_orig_name
            form.email.data = task.user.email

        return render_template('tryagain.html', form=form, token=token, error=error)
