# -*- coding: utf-8 -*-

from flask import request, Response, url_for
from flask.views import MethodView
from application.common.token_serialize import deserialize
from application.api.base import response_fail, response_ok, response_json
from application.config.messages import get_message, TWILIO_STATUSES
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

        session.commit()
        task = session.query(Task).get(data.get('task_id', -1))

        if not task:
            return response(*response_fail(message=get_message('NOT_FOUND')))

        if dataset == 'fax_requested':
            return response(*response_ok())
        elif dataset == 'email_verified':
            return response(*response_json(success=task.user.confirmed_at))
        elif dataset == 'fax_queued':
            message, data = None, None

            if task.status == Task.STATUS_UNCONFIRMED:
                message = get_message('TASK_UNCONFIRMED')
            elif task.status == Task.STATUS_FAILED:
                message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                      fax=task.fax,
                                      reason=(TWILIO_STATUSES.get(task.twilio_status) or TWILIO_STATUSES.get('failed')))
            elif task.status == Task.STATUS_PENDING:
                data = {'in_progress': True}

            return response(*response_json(success=not bool(message), message=message, data=data))
        elif dataset == 'fax_being_transmitted':
            message, data = None, None

            if task.status == Task.STATUS_QUEUED:
                data = {'in_progress': True}

            return response(*response_ok(message=message, data=data))
        elif dataset == 'fax_sent':
            message = None

            if task.status == Task.STATUS_FAILED:
                message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                      fax=task.fax,
                                      reason=(TWILIO_STATUSES.get(task.twilio_status) or TWILIO_STATUSES.get('failed')))

            return response(*response_json(success=(task.status == Task.STATUS_SENT), message=message))
