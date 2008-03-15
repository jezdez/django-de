import os
import datetime
import urlparse
from django.conf import settings
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django_de.apps.documentation.models import Release, _get_svnroot
from django_de.apps.documentation import builder

def index(request, version=None):
    template_list = ["documentation/%s_index.html" % version, "documentation/index.html"]
    return render_to_response(template_list, {"version": version,}, RequestContext(request, {}))

def detail(request, slug, version=None):
    try:
        import pysvn
    except ImportError:
        raise Http404("PySVN not found")
    else:
        client, version, docroot = _get_svnroot(version, settings.DOCS_SVN_PATH)

        docpath = urlparse.urljoin(docroot, slug+".txt")
        try:
            name, info = client.info2(docpath)[0]
        except pysvn.ClientError:
            raise Http404("Invalid doc: %r (version %r)" % (slug, version))

        parts = builder.build_document(client.cat(docpath))
        template_list = ["documentation/%s_detail.html" % version, "documentation/detail.html"]
        context = {
            "doc": parts,
            "revision": info.rev.number,
            "all_versions": Release.objects.all(),
            "slug": slug,
            "version": version,
            "update_date": datetime.datetime.fromtimestamp(info.last_changed_date),
        }
        return render_to_response(template_list, context, RequestContext(request, {}))
