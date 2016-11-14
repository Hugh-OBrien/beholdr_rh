from __future__ import absolute_import, unicode_literals
from os import environ as env_var
from .base import *

DEBUG = False

SECRET_KEY = env_var.get('beholdr_rh')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
