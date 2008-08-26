# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.db.models import permalink
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.template.defaultfilters import capfirst, slugify
from django.contrib import admin

from django.http import HttpResponseNotFound

from tagging.models import Tag, TaggedItem
from tagging.fields import TagField

from comments.models import Comment
from weblog import textutils

STATUS = (
    ('DRAFT', _('Draft')),
    ('CLOSED', _('Closed')),
    ('OPEN', _('Public')),
)

COMMENT_STATUS = (
    ('OPEN', _('Open (New comments allowed)')),
    ('CLOSED', _('Closed (No new comments allowed)')),
    ('HIDDEN', _('Hidden (Hide comments and comment-form)')),
)

class EntryManager(models.Manager):

    def this_site(self):
        return self.filter(site=Site.objects.get_current())

    def entries_by_user(self, request=None):
        # User mit "edit_foreign" Rechten, kann alle Drafts und öffentlichen Artikel sehen
        try:
            if request.user.has_perm('collticker.change_foreign'):
                return self.this_site().filter(status__in=['OPEN', 'DRAFT'])
    
            # Normaler Schreiber, kann nur seine eigenen (Auch Drafts) und die Öffentlichen Artikel sehen
            if request.user.has_perm('collticker.add_entry'):
                return self.this_site().filter(Q(status='OPEN') | Q(status='DRAFT', author=request.user))
        except AttributeError:
            # Keine Rechte = Sieht nur die öffentlichen Artikel
            return self.this_site().filter(status='OPEN')
        else:
            return self.this_site().filter(status='OPEN')
            
    def timetable(self):
        dates = self.active().dates('published', 'month')
        return dates


class Entry(models.Model):

    objects = EntryManager()

    # Title and Slug
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), blank=True)

    content = models.TextField(_('Content'))
    content_processed = models.TextField(_('Processed Content'), blank=True)
    source_url = models.URLField(_('Source URL'), blank=True)

    # Date Fields
    published = models.DateTimeField(_('Published'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    # Status Fields
    status = models.CharField(_('Status'),
        max_length=6,
        choices=STATUS,
        default='DRAFT')

    comment_status = models.CharField(_('Comment Status'),
        max_length=6,
        choices=COMMENT_STATUS,
        default='OPEN')

    language = models.CharField(_('Language'),
        max_length=5,
        choices=settings.LANGUAGES,
        default=settings.LANGUAGE_CODE
    )

    # Related
    tags = TagField()
    author = models.ForeignKey(User)
    site = models.ForeignKey(Site, default=settings.SITE_ID)

    # Comments
    comments = generic.GenericRelation(Comment)

    class Meta:
        ordering = ('-published',)
        permissions = (
            ('change_foreign', 'Can change foreign entry'),
            ('change_status', 'Can set status'),
            ('publish_instantly', 'Publish instantly'),
        )

    def get_author(self):
        if self.author.first_name:
            return "%s %s" % (self.author.first_name, self.author.last_name)
        else:
            return self.author.username

    def get_comments(self):
        return self.comments.active()

    def get_comment_count(self):
        return self.get_comments().count()

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def get_related(self):
        return TaggedItem.objects.get_related(self, Entry.objects.entries_by_user(request=None))

    def get_related_tags(self):
        return Tag.objects.related_for_model(self.tags, Entry)

    def get_next(self):
        return self.get_next_by_published(status='OPEN')

    def get_prev(self):
        return self.get_previous_by_published(status='OPEN')

    def __unicode__(self):
        return self.title

    def save(self):
        self.slug = slugify(self.title)
        self.content_processed = textutils.textfilter(self.content)
        super(Entry, self).save()

    @permalink
    def get_absolute_url(self):
        return ('weblog_details', (), {
            'id': str(self.id),
            'slug': self.slug,
        })

class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'status',
        'published',
        'author',
    )

admin.site.register(Entry, EntryAdmin)
