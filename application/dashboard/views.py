# -*- coding: utf-8 -*-

from flask import render_template, abort
from flask.views import MethodView
from application.common.token_serialize import deserialize
from application.models import User, Task
from application.database import session


class DashboardMethodView(MethodView):
    def get(self, token):
        _, _, data = deserialize(token)

        user = session.query(User).get(data.get('user_id'))

        if not user:
            abort(404)

        tasks = session.query(Task).filter(Task.user_id == user.id, Task.status == Task.STATUS_SENT)

        return render_template('dashboard.html', user=user, tasks=tasks)
