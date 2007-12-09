import os
import urlparse
import pysvn
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response

from django_de.apps.documentation.models import Release, Documentation

def get_svnroot(version, subpath):
    client = pysvn.Client()

    if subpath is None:
        docroot = settings.DOCS_SVN_ROOT
    else:
        if version is None:
            version = "trunk"
            subpath = os.path.join(subpath, "trunk/")
        else:
            rel = get_object_or_404(Release, version=version)
            subpath = os.path.join(subpath, rel.repository_path)
        docroot = urlparse.urljoin(settings.DOCS_SVN_ROOT, subpath)

    try:
        client.info2(docroot, recurse=False)
    except pysvn.ClientError:
        raise Http404("Bad SVN path: %s" % docroot)
    return client, version, docroot

