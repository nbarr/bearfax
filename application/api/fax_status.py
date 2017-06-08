# -*- coding: utf-8 -*-

from flask import request, Response, url_for
from flask.views import MethodView
from application.common.token_serialize import deserialize
from application.api.base import response_fail, response_ok, response_json
from application.config.messages import get_message
from application.models import Task
from application.database import session


def response(data, code, mimetype):
    return Response(data, status=code, mimetype=mimetype)


class FaxStatusApi(MethodView):
    def get(self):
        dataset = request.args.get('dataset')
        token = request.args.get('token')

        expired, invalid, data = deserialize(token)

        if invalid or not data:
            return response(*response_fail(message=get_message('NOT_FOUND')))

        task = session.query(Task).get(data.get('task_id', -1))
        if not task:
            return response(*response_fail(message=get_message('NOT_FOUND')))

        if dataset == 'fax_requested':
            return response(*response_ok())
        elif dataset == 'email_verified':
            return response(*response_json(success=task.user.confirmed_at))
        elif dataset == 'fax_queued':
            # TODO: think twice, maybe it shouls be shown on "step 4" card?
            message = ''

            if task.status == Task.STATUS_UNCONFIRMED:
                message = get_message('TASK_UNCONFIRMED')
            elif task.status == Task.STATUS_FAILED:
                message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token))

            return response(*response_json(success=not bool(message), message=message))
        elif dataset == 'fax_being_transmitted':
            # TODO: really don't know how to detect this step
            pass
        elif dataset == 'fax_sent':
            return response(*response_json(success=(task.status == Task.STATUS_SENT)))
