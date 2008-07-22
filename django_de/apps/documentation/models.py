import os
import urlparse

from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404

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
            docroot = urlparse.urljoin(
                settings.DOCS_SVN_ROOT,
                settings.DOCS_SVN_PATH)
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
