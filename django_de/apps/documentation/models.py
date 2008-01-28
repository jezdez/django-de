import os
import urlparse
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.dispatch import dispatcher
from django.core.mail import mail_admins

from django_de.signals import post_commit, pre_commit
from django_de.apps.documentation import builder
from django_de.generator import quick_publish, quick_delete, StaticGeneratorException

def get_choices(path=None):
    try:
        import pysvn
    except ImportError:
        yield (None, None)
    else:
        client, version, root = _get_svnroot(None, path)
        choicelist = client.ls(root, recurse=False)
        choicelist = [os.path.splitext(os.path.basename(choice.name))[0] for choice in choicelist]
        choicelist.sort()
        choices = []
        for choice in choicelist:
            choices.append((choice, choice))
        for choice in choices:
            yield choice

class Release(models.Model):
    version = models.CharField(_("version"), max_length=20, unique=True, choices=get_choices())
    release_date = models.DateField(_("release date"))

    class Meta:
        ordering = ('-release_date',)

    class Admin:
        list_display = ("version", "release_date")

    def __unicode__(self):
        return self.version

    def get_absolute_url(self):
        return ('django_de.apps.documentation.views.index', [self.version])
    get_absolute_url = permalink(get_absolute_url)

def _get_svnroot(version, subpath):
    try:
        import pysvn
    except ImportError:
        pass
    else:
        client = pysvn.Client()
        if subpath is None:
            docroot = urlparse.urljoin(settings.DOCS_SVN_ROOT, settings.DOCS_SVN_PATH)
        else:
            if version is None:
                version = "trunk"
                subpath = os.path.join(subpath, "trunk/")
            else:
                rel = get_object_or_404(Release, version=version)
                subpath = os.path.join(subpath, rel.version+"/")
            docroot = urlparse.urljoin(settings.DOCS_SVN_ROOT, subpath)

        try:
            client.info2(docroot, recurse=False)
        except pysvn.ClientError:
            raise Http404("Bad SVN path: %s" % docroot)
        return client, version, docroot

def get_documents():
    """
    Returns a list of document slugs available in the SVN.
    """
    for release in Release.objects.all():
        client, version, docroot = _get_svnroot(release.version, settings.DOCS_SVN_PATH)
        doclist = client.ls(docroot, recurse=False)
        doclist = [os.path.splitext(os.path.basename(doc.name))[0] for doc in doclist]
        doclist.sort()
        return tuple(["/documentation/%s/" % doc for doc in doclist])

def generate_static_docs(signal, repo, rev):
    mail_admins("Yeah: SVN commit!", e, fail_silently=True)
    for release in Release.objects.all():
        urls = get_documents(release.version)
        try:
            if signal == pre_commit:
                quick_delete(urls)
            elif signal == post_commit:
                quick_publish(urls)
        except StaticGeneratorException, e:
            mail_admins("Error: SVN commit", e, fail_silently=True)
            sys.exit(e)

dispatcher.connect(generate_static_docs, signal=post_commit)
dispatcher.connect(generate_static_docs, signal=pre_commit)
