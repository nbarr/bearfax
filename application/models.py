# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import backref, relationship
from flask_security import RoleMixin, UserMixin


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

    STATUS_QUEUED = 'queued'
    STATUS_EXPIRED = 'expired'
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'

    id = Column(Integer(), primary_key=True)

    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref=backref('tasks', cascade='all, delete-orphan'), uselist=False)

    document_orig_name = Column(String(length=100), nullable=False)
    document_name = Column(String(length=150), nullable=False, unique=True)
    prefix = Column(String(length=50), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    status = Column(String(length=10), nullable=True)
    attempts = Column(Integer(), nullable=True)
    url = Column(String(length=300), nullable=False)
    fax = Column(String(length=20), nullable=False)
