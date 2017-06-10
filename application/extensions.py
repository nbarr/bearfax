# -*- coding: utf-8 -*-

from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_security import Security
from flask_socketio import SocketIO


security = Security()
csrf = CSRFProtect()
mail = Mail()
socketio = SocketIO()
