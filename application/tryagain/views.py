# -*- coding: utf-8 -*-

from flask import abort, render_template
from flask.views import MethodView
from application.common.token_serialize import deserialize
from application.models import Task
from application.database import session
from application.tryagain.forms import TryAgainForm


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

        return render_template('tryagain.html', form=form)

    def post(self, token):
        pass
