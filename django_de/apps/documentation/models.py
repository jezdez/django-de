import os
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django_de.apps.authors.models import Author
from django_de.apps.documentation import builder
from django_de.apps.documentation.utils import get_svnroot

def get_choices(path=None):
    from django_de.apps.documentation.utils import get_svnroot
    client, version, root = get_svnroot(None, path)
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
    repository_path = models.CharField(_("repository path"), max_length=50, help_text="(i.e. '0.95' or 'trunk')")
    release_date = models.DateField(_("release date"))

    class Meta:
        ordering = ('-release_date',)

    class Admin:
        list_display = ("version", "repository_path", "release_date")

    def __unicode__(self):
        return self.version

    def get_absolute_url(self):
        return ('django_de.apps.documentaion.views.doc_index', [self.version])
    get_absolute_url = permalink(get_absolute_url)

class Documentation(models.Model):
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('document'), help_text=_('Available documentation files in SVN repository'), choices=get_choices(settings.DOCS_SVN_PATH))
    release = models.ForeignKey(Release, help_text=_("Belongs to which Django release?"))
    authors = models.ManyToManyField(Author, verbose_name=_('authors'))
    summary = models.TextField(_('description'), help_text=_('HTML please, in a p tag'))
    order = models.SmallIntegerField(_('position in the index'))

    class Admin:
        list_display = ('title', 'slug')
        list_filter = ('authors')
        search_fields = ('title', 'summary')

    class Meta:
        ordering = ('order', 'slug', 'title')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
         return ('django_de.apps.documentation.views.doc_detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)

    def save(self):
        client, version, docroot = get_svnroot(self.release.version, settings.DOCS_SVN_PATH)
        docpath = urlparse.urljoin(docroot, self.slug+".txt")
        try:
            name, info = client.info2(docpath)[0]
        except pysvn.ClientError:
            self.title = self.slug
            super(Documentation, self).save()
        cache_key = "django_de:docs:%s:%s:%s" % (self.release.version, self.slug, info.rev.number)
        parts = cache.get(cache_key)
        if parts is None:
            parts = builder.build_document(client.cat(docpath))
            cache.set(cache_key, parts, 60*60)
        self.title = parts["title"]
        super(Documentation, self).save()
