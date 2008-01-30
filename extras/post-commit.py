#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, "/home/django-de/lib")
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.core.mail import mail_admins
from django_de.apps.documentation.models import get_documents
from django_de.generator import StaticGenerator, StaticGeneratorException

def main():
    """
    Deletes or generates static documentation files depending on the
    received signal.
    """
    repo=sys.argv[1]
    rev=sys.argv[2]
    mail_admins("SVN revision %s committed!" % rev, "SVN repo: %s" % repo, fail_silently=True)
    try:
        for document in get_documents():
            gen = StaticGenerator((document,))
            gen.start()
    except StaticGeneratorException:
        mail_admins("Error: SVN commit", "error while generating static files", fail_silently=True)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s REPOS TXN\n" % (sys.argv[0]))
    else:
        main()
