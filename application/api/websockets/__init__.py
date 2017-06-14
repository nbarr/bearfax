# -*- coding: utf-8 -*-

from flask_socketio import emit
from application.extensions import socketio
from application.api.websockets import check_task_status


def configure_websockets(app):
    @socketio.on_error_default
    def default_error_handler(e):
        raise RuntimeError()

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    socketio.on_event(
        check_task_status.CHECK_STATUS_EVENT,
        check_task_status.event_handler,
        namespace=check_task_status.TASK_STATUS_NAMESPACE
    )

    @socketio.on('test')
    def handle_test_event(data):
        print('>> Test event received:', str(data))

        emit('test_response', {'receive': 1})
