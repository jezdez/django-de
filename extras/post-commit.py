#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib/python2.4/site-packages'))
path = site.addsitedir(lib_path, set())
if path:
    sys.path = list(path) + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.core.management import call_command
from django.core.mail import mail_admins

def main():
    """
    Deletes or generates static documentation files depending on the
    received signal.
    """
    repo, rev = sys.argv[1:3]
    mail_admins("SVN revision %s committed!" % rev, "SVN repo: %s\nhttps://www.django-de.org/trac/changeset/%s/" % (repo, rev), fail_silently=True)
    call_command('deletestatic', **{'repo': repo, 'rev': rev})

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s REPOS TXN\n" % (sys.argv[0]))
    else:
        main()
