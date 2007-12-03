#! -*- encoding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

LANGUAGES = (
	('Fr', _('French')),
	('En', _('English')),
	('De', _('German')),
)

class LinkManager(models.Manager):
	def get_query_set(self):
		""" Retrieve only published links. """
		qs = super(LinkManager, self).get_query_set()
		return qs.filter(is_online=True)

class Link(models.Model):
	title = models.CharField('Titre', maxlength=200)
	slug = models.SlugField( _('slug'), prepopulate_from=('title',), help_text=_('for direct access from the link page.'))
	url = models.URLField(_('link url'), help_text=_('url of the linked resource'))
	lang = models.CharField(_('link language'), maxlength=2, choices=LANGUAGES, default='En')
	comment = models.TextField(_('comment'), help_text=_('small descriptive text'))
	submission_date = models.DateTimeField(_('submission date'))

	is_online = models.BooleanField(_('published'), default=False)
	related_tags = TagField(help_text=_('space- or comma-seperated tags'))

	class Admin:
		list_display = ('title', 'url', 'is_online')
		list_filter = ('submission_date', 'is_online')
		search_fields = ('title', 'comment')
		date_hierarchy = 'submission_date'

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return "/liens/%s/#%s" % (self.submission_date.strftime("%Y/%m"), self.slug)

	def _get_tags(self):
		return Tag.objects.get_for_object(self)

	def _set_tags(self, tag_list):
		return Tag.objects.update_tags(self, tag_list)

	tags = property(_get_tags, _set_tags)

	objects = models.Manager()
	published = LinkManager()

