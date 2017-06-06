# -*- coding: utf-8 -*-

import os

# Here stored settings related to Flask instance and extensions
# Normally this file should not be imported anywhere

SECRET_KEY = 'd+/6n~G@]gt.&j"%pku?5<7?GcP;?fDn-3)%cg~g&NN%3LmhH#fmW!A(\4a8Vr%ff4%ZHMk&(J(54q_'
DEBUG = os.getenv('ENVIRONMENT') != 'production'

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = '2d47a98bf26049cfae5656e2b244e8eb2d47a98bf26049cfae5656e2b244e8eb'
