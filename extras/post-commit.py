#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import threading

sys.path.insert(0, "/home/django-de/lib")
os.environ['DJANGO_SETTINGS_MODULE'] = "django_de.settings"

from django.core.mail import mail_admins
from django_de.apps.documentation.models import get_documents
from django_de.generator import quick_publish, StaticGeneratorException

class StaticFilesThread(threading.Thread):
    """
    Starts the generation of static files for faster SVN committs.
    """
    def __init__(self, repo, rev):
        threading.Thread.__init__(self)
        self.repo = repo
        self.rev = rev

    def run(self):
        """
        Deletes or generates static documentation files depending on the
        received signal.
        """
        mail_admins("SVN revision %s committed!" % self.rev, "SVN repo: %s" % self.repo, fail_silently=True)
        urls = get_documents()
        try:
            quick_publish(urls)
        except StaticGeneratorException:
            mail_admins("Error: SVN commit", "error while generating static files", fail_silently=True)

def main():
    static_file_generator = StaticFilesThread(repo=sys.argv[1], rev=sys.argv[2])
    static_file_generator.start()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s REPOS TXN\n" % (sys.argv[0]))
    else:
        main()
