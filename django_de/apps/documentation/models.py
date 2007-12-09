import os
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django_de.apps.authors.models import Author

class Release(models.Model):
    version = models.CharField(_("version"), maxlength=20, unique=True)
    repository_path = models.CharField(_("repository path"), maxlength=50, help_text="(i.e. '0.95' or '0.95-bugfixes')")
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

def get_choices(path=None):
    from utils import get_svnroot
    client, version, root = get_svnroot(None, path)
    choicelist = client.ls(root, recurse=False)
    choicelist = [os.path.splitext(os.path.basename(choice.name))[0] for choice in choicelist]
    choicelist.sort()
    choices = []
    for choice in choicelist:
        choices.append((choice, choice))
    for choice in choices:
        yield choice    

class Documentation(models.Model):
    slug = models.SlugField(_('slug'), help_text=_('used for URL'), choices=get_choices(settings.DOCS_SVN_PATH))
    version = models.CharField(_('version'), max_length=20, choices=get_choices())

    release = models.ForeignKey(Release)
    authors = models.ManyToManyField(Author, verbose_name=_('authors'))

    summary = models.TextField(_('description'), help_text=_('HTML please, in a p tag'))
    order = models.SmallIntegerField(_('position in the index'))

    class Admin:
        list_display = ('slug', 'version')
        list_filter = ('authors',)
        search_fields = ('slug', 'summary', 'version')

    class Meta:
        ordering = ('order', 'slug')

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
         return ('django_de.apps.documentation.views.doc_detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)
