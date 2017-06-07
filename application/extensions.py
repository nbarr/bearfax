# -*- coding: utf-8 -*-

from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_security import Security


security = Security()
csrf = CSRFProtect()
mail = Mail()
