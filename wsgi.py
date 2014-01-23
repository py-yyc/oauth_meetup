#!/usr/bin/env python2.5
# coding: UTF-8

import os
import os.path
import sys
import time
import traceback

if sys.version < "2.7":
  python = os.path.join(os.environ['HOME'], 'local', 'bin', 'python2.7')
  os.execl(python, python, *sys.argv)

"""
WSGI config for polls project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
