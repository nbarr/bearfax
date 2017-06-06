# -*- coding: utf-8 -*-

from flask.views import MethodView
from application.api.base import response_fail, response_ok


class StatusApiView(MethodView):
    def get(self, task_id):
        return response_fail(message='Not ready yet...')
