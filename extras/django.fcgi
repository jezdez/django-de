#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
sys.stdout = sys.stderr

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lib/'))
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi()
