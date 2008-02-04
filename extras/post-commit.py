#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, "/home/django-de/lib")
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.core.management import call_command
from django.core.mail import mail_admins

def main():
    """
    Deletes or generates static documentation files depending on the
    received signal.
    """
    repo, rev = sys.argv[1:2]
    mail_admins("SVN revision %s committed!" % rev, "SVN repo: %s" % repo, fail_silently=True)
    call_command('generatestatic', **{'repo': repo, 'rev': rev})
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s REPOS TXN\n" % (sys.argv[0]))
    else:
        main()
