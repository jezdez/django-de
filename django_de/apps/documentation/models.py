from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from django_de.apps.documentation.utils import restify
from django_de.apps.authors.models import Author
from tagging.fields import TagField
from tagging.models import Tag

class Documentation(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), help_text='Conserver celle du site officiel.')
    version = models.CharField(_('version'), max_length=10)
    revision = models.PositiveIntegerField(_('revision'))

    authors = models.ManyToManyField(Author, verbose_name=_('authors'))

    summary = models.TextField(_('description'), help_text=_('HTML please, in a p tag'))
    content = models.TextField(_('content'), help_text=_('only ReST markup please'))
    toc_html = models.TextField(_('menu HTML'), blank=True)
    content_html = models.TextField(_('content HTML'), blank=True)

    order = models.SmallIntegerField(_('position in the index'))
    related_tags = TagField(help_text=_('space- or comma-seperated tags'))

    class Admin:
        list_display = ('title', 'version', 'revision')
        list_filter = ('authors',)
        search_fields = ('title', 'content', 'summary')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
         return ('django.views.generic.list_detail.object_detail', [self.slug])
    get_absolute_url = permalink(get_absolute_url)

    def save(self):
        # deal with ReSTification
        self.toc_html, self.content_html = restify(self.content)
        super(Documentation, self).save() # Call the "real" save() method.

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tag_list):
        return Tag.objects.update_tags(self, tag_list)

    tags = property(_get_tags, _set_tags)
