# -*- coding: utf-8 -*-

from flask import url_for, current_app
from flask_socketio import emit
from application.common.token_serialize import deserialize
from application.api.base import response_fail, response_ok, response_json
from application.config.messages import get_message, TWILIO_STATUSES
from application.models import Task
from application.database import session
from application.cron import process_pending, process_queued


TASK_STATUS_NAMESPACE = '/task_status'
CHECK_STATUS_EVENT = 'check_task_status'
TASK_STATUS_RESPONSE = 'task_status_response'


def event_handler(req_data):
    def response(response_data, code, mimetype):
        emit(TASK_STATUS_RESPONSE, response_data, namespace=TASK_STATUS_NAMESPACE)

    print('>> received check_task_status: ' + str(req_data))

    dataset = req_data.get('dataset')
    token = req_data.get('token')

    expired, invalid, data = deserialize(token)

    if invalid or not data:
        return response(*response_fail(message=get_message('NOT_FOUND')))

    # NOTE: Do not remove this line. It notifying SQLAlchemy that session's object is dirty
    session.commit()

    try:
        task = session.query(Task).filter(Task.task_uid == data.get('task_uid', -1)).one()
    except:
        return response(*response_fail(message=get_message('NOT_FOUND')))

    if not task:
        return response(*response_fail(message=get_message('NOT_FOUND')))

    if dataset == 'fax_requested':
        return response(*response_ok())
    elif dataset == 'email_verified':
        return response(*response_json(success=bool(task.user.confirmed_at)))
    elif dataset == 'fax_queued':
        message, data = None, None

        if task.status == Task.STATUS_UNCONFIRMED:
            message = get_message('TASK_UNCONFIRMED')
        elif task.status == Task.STATUS_FAILED:
            message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                  fax=task.fax,
                                  reason=(TWILIO_STATUSES.get(task.twilio_status) or TWILIO_STATUSES.get('failed')))
        elif task.status == Task.STATUS_PENDING:
            result = process_pending(current_app.logger, task.task_uid)

            if result is None:
                message = get_message('QUEUE_FULL')

            if task.status == Task.STATUS_PENDING:
                data['in_progress'] = True
            elif task.status == Task.STATUS_FAILED:
                message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                      fax=task.fax,
                                      reason=(TWILIO_STATUSES.get(task.twilio_status) or task.twilio_status))

        return response(*response_json(success=not bool(message), message=message, data=data))
    elif dataset == 'fax_being_transmitted':
        success, message, data = True, None, None

        if task.status == Task.STATUS_FAILED:
            message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                  fax=task.fax,
                                  reason=(TWILIO_STATUSES.get(task.twilio_status) or TWILIO_STATUSES.get('failed')))
            success = False
        elif task.status == Task.STATUS_QUEUED:
            result = process_queued(current_app.logger, task.task_uid)

            if task.status == Task.STATUS_QUEUED:
                data['in_progress'] = True
            elif task.status == Task.STATUS_FAILED:
                message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                      fax=task.fax,
                                      reason=(TWILIO_STATUSES.get(task.twilio_status) or task.twilio_status))

            if result == 0:
                message = get_message('SILL_SENDING')

        return response(*response_json(success=success, message=message, data=data))
    elif dataset == 'fax_sent':
        message = None

        if task.status == Task.STATUS_FAILED:
            message = get_message('TASK_FAILED', url=url_for('views.tryagain', token=token),
                                  fax=task.fax,
                                  reason=(TWILIO_STATUSES.get(task.twilio_status) or TWILIO_STATUSES.get('failed')))
        return response(*response_json(success=(task.status == Task.STATUS_SENT), message=message))

    return response(*response_fail(message=get_message('BAD_DATASET', dataset=dataset)))
