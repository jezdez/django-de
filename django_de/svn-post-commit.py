#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.expanduser("~/lib"))
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django_de.apps.documentation.models import Release
from django_de.apps.documentation.views import get_documents
from django_de.generator import quick_publish, quick_delete, StaticGeneratorException

for release in Release.objects.all():
    urls = ["%s%s/" % (release.get_absolute_url(), doc) for doc in get_documents(release.version)]
    try:
        # Cleaning up the static documentation files
        quick_delete(urls)
    except StaticGeneratorException:
        pass
    try:
        # Publishing new versions
        quick_publish(urls)
    except StaticGeneratorException:
        pass
