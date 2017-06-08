# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table, event
from sqlalchemy.orm import backref, relationship
from flask import current_app
from flask_security import RoleMixin

from application.config.flask_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_KEY_ID, AWS_BUCKET
from application.common.s3files import s3_delete_file

Base = declarative_base()


roles_to_users = Table(
    'roles_to_users',
    Base.metadata,
    Column('user_id', Integer(), ForeignKey('users.id')),
    Column('role_id', Integer(), ForeignKey('roles.id'))
)


class Role(Base, RoleMixin):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    name = Column(String(length=100), unique=True)
    description = Column(String(length=255))

    def __str__(self):
        return self.name


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    email = Column(String(50), nullable=False)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary=roles_to_users, backref=backref('users'))

    def __str__(self):
        return self.email


class Task(Base):
    __tablename__ = 'tasks'

    STATUS_UNCONFIRMED = 'unconfirmed'
    STATUS_PENDING = 'pending'
    STATUS_QUEUED = 'queued'
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'

    id = Column(Integer(), primary_key=True)

    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('tasks', cascade='all, delete-orphan'), uselist=False)

    status = Column(String(length=10), nullable=True)

    document_orig_name = Column(String(length=100), nullable=False)
    document_name = Column(String(length=150), nullable=False, unique=True)
    prefix = Column(String(length=50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    attempts = Column(Integer(), nullable=True)
    url = Column(String(length=300), nullable=False)
    fax = Column(String(length=20), nullable=False)
    fax_sid = Column(String(length=50))


class LogInfo(Base):
    __tablename__ = 'loginfos'

    EVENT_USER_ADDED = 'user_added'
    EVENT_CONFIRM_EMAIL_SENT = 'confirmation_sent'
    EVENT_STATUS_CHANGED = 'task_status_changed'
    EVENT_TWILIO_REQUEST_SUBMITED = 'twilio_request_submited'
    EVENT_TWILIO_RESPONSE_RECEIVED = 'twilio_response_received'

    id = Column(Integer(), primary_key=True)

    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('logs', cascade='all, delete-orphan'), uselist=False)

    task_id = Column(Integer(), ForeignKey('tasks.id'), nullable=True)
    task = relationship('Task', backref=backref('logs', cascade='all, delete-orphan'), uselist=False)

    event = Column(String(length=30), nullable=False)
    field = Column(String(length=50))
    original_value = Column(String(length=100))
    new_value = Column(String(length=100))

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# Events


def _log_exception(message, *args):
    try:
        current_app.logger.exception(message, ex)
    except:
        pass


@event.listens_for(Task, 'before_delete')
def on_before_task_delet(mapper, connection, target):
    print('Removing associated file from S3', target.prefix, target.document_name)
    s3_delete_file(AWS_ACCESS_KEY_ID, AWS_SECRET_KEY_ID, AWS_BUCKET, target.document_name, target.prefix)


@event.listens_for(User, 'after_insert')
def on_after_user_created(mapper, connection, target):
    try:
        connection.execute(
            LogInfo.__table__.insert(),
            user_id=target.id,
            event=LogInfo.EVENT_USER_ADDED,
            created_at=datetime.utcnow()
        )
    except Exception as ex:
        _log_exception('Unable log changes for event "{}": "{}"'.format(LogInfo.EVENT_USER_ADDED, ex), ex)


@event.listens_for(Task, 'before_update')
def on_before_information_review_updated(mapper, connection, target):
    try:
        prev = connection.execute(Task.__table__.select(), id=target.id).first()

        if prev.status != target.status:
            connection.execute(
                LogInfo.__table__.insert(),
                user_id=target.user.id,
                event=LogInfo.EVENT_STATUS_CHANGED,
                field='status',
                original_value=prev.status,
                new_value=target.status,
                created_at=datetime.utcnow()
            )

    except Exception as ex:
        _log_exception('Unable to log changes for event "{}": "{}"'.format(LogInfo.EVENT_STATUS_CHANGED, ex), ex)
