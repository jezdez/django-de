#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import site
sys.stdout = sys.stderr

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib/python2.4/site-packages'))
path = site.addsitedir(lib_path, set())
if path:
    sys.path = list(path) + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_de.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
