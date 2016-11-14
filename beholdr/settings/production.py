from __future__ import absolute_import, unicode_literals

import os

from .base import *

DEBUG = False

SECRET_KEY=os.environ['beholdr_rh']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
