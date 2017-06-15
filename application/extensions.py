# -*- coding: utf-8 -*-

from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_security import Security
from flask_socketio import SocketIO
from flask_recaptcha import ReCaptcha

security = Security()
csrf = CSRFProtect()
mail = Mail()
socketio = SocketIO()
recaptcha = ReCaptcha()