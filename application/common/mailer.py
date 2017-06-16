# -*- coding: utf-8 -*-

from flask import render_template, url_for, current_app
from flask_mail import Message
from application.extensions import mail
from application.database import session
from application.models import LogInfo
from application.common.token_serialize import serialize


def render(template_key, **kwargs):
    html, text, subj = '', '', ''

    try:
        html = render_template('{}_body.html'.format(template_key), **kwargs)
    except:
        pass

    try:
        text = render_template('{}_body.txt'.format(template_key), **kwargs)
    except:
        pass

    try:
        subj = render_template('{}_subj.txt'.format(template_key), **kwargs)
    except:
        pass

    return html, text, subj


def send_confirmation_mail(recipients, task, token):
    html, text, subj = render('mail/confirmation', task=task, token=token)
    msg = Message(subj, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=recipients)
    msg.html = html
    msg.body = text

    mail.send(msg)

    loginfo = LogInfo(
        user_id=task.user.id,
        task_id=task.id,
        event=LogInfo.EVENT_CONFIRM_EMAIL_SENT,
    )
    session.add(loginfo)
    session.commit()


def send_on_fax_sent_email(recipients, task):
    html, text, subj = render('mail/fax_sent', task=task)

    token = serialize({'user_id': task.user.id})

    msg = Message(subj, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=recipients, token=token)
    msg.html = html
    msg.body = text

    mail.send(msg)

    loginfo = LogInfo(
        user_id=task.user.id,
        task_id=task.id,
        event=LogInfo.EVENT_FAX_SUCCESSFULLY_SENT,
    )
    session.add(loginfo)
    session.commit()
