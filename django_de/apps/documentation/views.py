import os
import datetime
import urlparse
from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django_de.apps.documentation.models import Release
from django_de.apps.documentation import builder

def index(request, version=None):
    client, version, docroot = _get_svnroot(version, settings.DOCS_SVN_PATH)
    doclist = client.ls(docroot, recurse=False)
    
    # Convert list of URLs to list of document slugs.
    doclist = [os.path.splitext(os.path.basename(doc.name))[0] for doc in doclist]
    doclist.sort()
    
    template_list = ["documentation/%s_index.html" % version, "documentation/index.html"]
    context ={
        "version": version,
        "all_versions": Release.objects.all(),
        "document_list": doclist
    }
    return render_to_response(template_list, context, RequestContext(request, {}))

def detail(request, slug, version=None):
    client, version, docroot = _get_svnroot(version, settings.DOCS_SVN_PATH)

    docpath = urlparse.urljoin(docroot, slug+".txt")
    try:
        name, info = client.info2(docpath)[0]
    except pysvn.ClientError:
        raise Http404("Invalid doc: %r (version %r)" % (slug, version))
        
    cache_key = "django_de:docs:%s:%s:%s" % (version, slug, info.rev.number)
    parts = cache.get(cache_key)
    if parts is None:
        parts = builder.build_document(client.cat(docpath))
        cache.set(cache_key, parts, 60*60)
    
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
