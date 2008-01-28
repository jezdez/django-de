#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/home/django-de/lib")
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.dispatch import dispatcher
from django_de.signals import post_commit

def main():
    dispatcher.send(signal=post_commit, sender=None, repo=sys.argv[1], rev=sys.argv[2])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s REPOS TXN\n" % (sys.argv[0]))
    else:
        main()
