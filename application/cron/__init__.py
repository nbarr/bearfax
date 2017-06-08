# -*- coding: utf-8 -*-

"""
Cron job implementation

Run in command line: python -c "import application.cron; application.cron.run()"
"""

import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from datetime import datetime, timedelta
from application.config import settings, flask_settings
from application.database import session
from application.models import Task, LogInfo
from application.common import sendfax


def cleanup_unconfirmed(logger):
    """Remove all unconfirmed items older then `settings.FAX_CONFIRMATION_EXPIRATION_SECONDS`
    """
    print('cleanup_unconfirmed')

    min_created_time = datetime.utcnow() - timedelta(seconds=settings.FAX_CONFIRMATION_EXPIRATION_SECONDS)
    outdated = session.query(Task).filter(
        (Task.status == Task.STATUS_UNCONFIRMED) &
        (Task.created_at < min_created_time)
    )

    for task in outdated:
        session.delete(task)

    session.commit()


def process_queued(logger):
    """Query Twilio API for currently enqueued tasks and update its status
    """
    print('process_queued')

    twilio_statuses_ok = ['delivered']
    twilio_statuses_failed = ['no-answer', 'busy', 'failed', 'canceled']

    queued = session.query(Task).filter(Task.status == Task.STATUS_QUEUED)

    try:
        for task in queued:
            fax = sendfax.get_fax(flask_settings.TWILIO_SID, flask_settings.TWILIO_AUTH_TOKEN, task.fax_sid)

            if fax.status in twilio_statuses_ok:
                task.status = Task.STATUS_SENT
            elif fax.status in twilio_statuses_failed:
                task.status = Task.STATUS_FAILED

            session.commit()
    except Exception as ex:
        logger.exception(ex)


def process_pending(logger):
    """Takes next QUEUED fax request and tries to send it
    """
    print('process_pending')

    twilio_statuses_queues = ['queued']

    queued = session.query(Task).filter(Task.status == Task.STATUS_QUEUED).count()
    amount_to_process = settings.TWILIO_QUEUE_CAPACITY - queued

    if amount_to_process <= 0:
        logger.info('Twilio queue is full (curent capacity is {})'.format(settings.TWILIO_QUEUE_CAPACITY))
        return

    tasks = session.query(Task).filter(
        Task.status == Task.STATUS_PENDING
    ).order_by(Task.created_at).limit(amount_to_process)

    try:
        for task in tasks:
            result = sendfax.send_fax(
                flask_settings.TWILIO_SID,
                flask_settings.TWILIO_AUTH_TOKEN,
                '+{}'.format(task.fax),
                flask_settings.TWILIO_PHONE,
                task.url
            )

            if result.status not in twilio_statuses_queues:
                task.status = Task.STATUS_FAILED
            else:
                task.fax_sid = result.sid
                task.status = Task.STATUS_QUEUED

            loginfo = LogInfo(
                user_id=task.user_id,
                task_id=task.id,
                event=LogInfo.EVENT_TWILIO_REQUEST_SUBMITED,
                field='fax_sid',
                original_value=result.sid
            )
            session.add(loginfo)
            session.commit()
    except Exception as ex:
        logger.exception(ex)


def run():
    print('Running cron job')

    logger = logging.getLogger('bearfax-cron')
    formatter = Formatter('%(asctime)s | %(levelname)7s | %(module)s:%(funcName)s:%(lineno)4s | %(message)s')
    handler = StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    handler = RotatingFileHandler('logs/flask.log', maxBytes=2 * 1024 * 1024, backupCount=1)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    cleanup_unconfirmed(logger)
    process_queued(logger)
    process_pending(logger)

