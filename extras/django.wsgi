#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import fnmatch

def locate(pattern, root=os.curdir):
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)

lib_path = os.path.join(os.path.dirname(__file__), '../lib/')

sys.path.insert(0, lib_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_de.settings'

from django_de import monitor
import django.core.handlers.wsgi

monitor.start(interval=1.0)
for f in locate("*.py", os.path.join(lib_path, 'django_de')):
    monitor.track(f)

application = django.core.handlers.wsgi.WSGIHandler()
