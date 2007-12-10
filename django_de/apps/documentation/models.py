import os
import urlparse
import pysvn
from django.core.cache import cache
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response

from django_de.apps.authors.models import Author
from django_de.apps.documentation import builder

def get_choices(path=None):
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
        return ('django_de.apps.documentaion.views.index', [self.version])
    get_absolute_url = permalink(get_absolute_url)

def _get_svnroot(version, subpath):
    client = pysvn.Client()
    if subpath is None:
        docroot = urlparse.urljoin(settings.DOCS_SVN_ROOT, settings.DOCS_SVN_PATH)
    else:
        if version is None:
            version = "trunk"
            subpath = os.path.join(subpath, "trunk/")
        else:
            rel = get_object_or_404(Release, version=version)
            subpath = os.path.join(subpath, rel.version)+"/"
        docroot = urlparse.urljoin(settings.DOCS_SVN_ROOT, subpath)
    try:
        client.info2(docroot, recurse=False)
    except pysvn.ClientError:
        raise Http404("Bad SVN path: %s" % docroot)
    return client, version, docroot

class Documentation(models.Model):
    title = models.CharField(_('title'), editable=False, max_length=200, blank=True)
    slug = models.SlugField(_('document'), help_text=_('Documentation file from live SVN repository'), choices=get_choices(settings.DOCS_SVN_PATH))
    release = models.ForeignKey(Release, help_text=_("Show the Django release version it belongs to"))
    authors = models.ManyToManyField(Author, verbose_name=_('authors'))
    summary = models.TextField(_('description'), help_text=_('HTML please, in a p tag'))
    order = models.SmallIntegerField(_('position in the index'))

    class Admin:
        list_display = ('title_and_version', 'slug')
        list_filter = ('authors',)
        search_fields = ('title', 'summary')

    class Meta:
        ordering = ('order', 'slug', 'title')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
         return ('django_de.apps.documentation.views.detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)

    def save(self):
        client, version, docroot = _get_svnroot(self.release.version, settings.DOCS_SVN_PATH)
        docpath = urlparse.urljoin(docroot, "%s.txt" % self.slug)
        try:
            name, info = client.info2(docpath)[0]
        except pysvn.ClientError:
            self.title = self.slug
            super(Documentation, self).save()
        else:
            cache_key = "django_de:docs:%s:%s:%s" % (version, self.slug, info.rev.number)
            parts = cache.get(cache_key)
            if parts is None:
                parts = builder.build_document(client.cat(docpath))
                cache.set(cache_key, parts, 60*60)
            self.title = parts["title"]
            super(Documentation, self).save()

    def title_and_version(self):
        if self.title:
            title = self.title
        else:
            title = self.slug
        return "%s (%s)" % (title, self.release.version)
    title_and_version.short_description = _('title')
    