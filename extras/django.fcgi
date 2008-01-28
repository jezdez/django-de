#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.stdout = sys.stderr

# ~/public_html zum PYTHONPATH hinzufügen
libdir = os.path.expanduser("~/lib")
sys.path.insert(0, libdir)

# Django settings-modul definieren 
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi()
