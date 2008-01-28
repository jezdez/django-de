#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/home/django-de/lib")
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django_de.apps.documentation.models import Release
from django_de.apps.documentation.views import get_documents
from django_de.generator import quick_delete, StaticGeneratorException

def main():
    for release in Release.objects.all():
        urls = ["%s%s/" % (release.get_absolute_url(), doc) for doc in get_documents(release.version)]
        try:
            quick_delete(urls)
        except StaticGeneratorException, e:
            from django.core.mail import mail_admins
            mail_admins("Error: SVN pre commit", e, fail_silently=True)
            sys.exit(e)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s REPOS TXN\n" % (sys.argv[0]))
    else:
        main()

