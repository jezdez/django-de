import os
from django.conf import settings
from django_de.apps.documentation.models import Release, _get_svnroot

def get_documents():
    """
    Returns a list of document slugs available in the SVN.
    """
    all_docs = []
    for release in Release.objects.all():
        client, version, docroot = _get_svnroot(release.version, settings.DOCS_SVN_PATH)
        doclist = client.ls(docroot, recurse=False)
        doclist = [os.path.splitext(os.path.basename(doc.name))[0] for doc in doclist]
        doclist.sort()
        all_docs.extend(["/documentation/%s/" % doc for doc in doclist])
    return tuple(all_docs)
