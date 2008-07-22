import re
import md5
from urlparse import urljoin
from urllib import quote

from django.db import models
from django.conf import settings
from django.template.defaultfilters import escape
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django_de.apps.aggregator.manager import FeedManager, ItemManager

class Feed(models.Model):
    # Manger
    objects = FeedManager()

    # Feed Info
    public = models.BooleanField(_('Public'), default=False)
    feed_url = models.URLField(_('Feed URL'), verify_exists=False)
    url = models.URLField(_('Homepage URL'))
    title = models.CharField(_('Homepage Title'), max_length=255)
    owner_email = models.EmailField(_('E-Mail'))

    # Admin-defined settings
    keyword_check = models.BooleanField(_('Check each entry for keywords (see below)'), default=True, help_text=_('If this is a weblog or a category-feed with only django-related entries, you may uncheck this.'))
    keywords = models.CharField(_('Keywords'), max_length=255, help_text=_('All lowercase, seperate by spaces'), default='django', blank=True)

    # Automatic
    errors = models.IntegerField(_('Error Counter'), default=0)

    # Timestamps
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-published',)

    def admin_action_checkbox(self):
        enabled = (self.errors >= settings.AGGREGATOR_MAX_ERRORS) and ' disabled="disabled"' or ''
        error = (self.errors >= settings.AGGREGATOR_MAX_ERRORS) and _('Broken!') or ''
        checkbox = '<input type="checkbox" name="item_id_list" value="%s"%s/> %s' % (self.id, enabled, error)
        return checkbox
    admin_action_checkbox.short_description = ''
    admin_action_checkbox.allow_tags = True

    def public_flag(self):
        return self.public
    public_flag.boolean = True
    public_flag.short_description = _('Public')

    def item_count(self):
        return self.item_set.count()
    item_count.short_description = _('Items')

    def keyword_check_flag(self):
        return self.keyword_check
    keyword_check_flag.boolean = True
    keyword_check_flag.short_description = _('KW Check')

    def url_link(self):
        return '<a href="%s" target="_blank">%s</a>' % (self.url, re.split(r'/', self.url)[2])
    url_link.allow_tags = True
    url_link.short_description = _('Link to Homepage')

    def get_gravatar_url(self):
        current_site_domain = Site.objects.get_current().domain

        # By default, Site-Domains don't start with http[s]://
        if not current_site_domain.startswith('http'):
            current_site_domain = 'http://%s' % current_site_domain

        # urljoin does not work the way like os.path.join
        image_url = urljoin(
            current_site_domain,
            urljoin(
                getattr(settings, 'MEDIA_URL', '/site_media/'),
                getattr(settings, 'AGGREGATOR_GRAVATAR_DEFAULT_IMAGE', 'gravatar.png'),
            )
        )

        return 'http://www.gravatar.com/avatar.php?gravatar_id=%s&default=%s&size=%s&rating=%s' % (
                md5.new(self.owner_email).hexdigest(),
                quote(image_url),
                getattr(settings, 'AGGREGATOR_GRAVATAR_SIZE', 50),
                getattr(settings, 'AGGREGATOR_GRAVATAR_RATING', 'G'),
        )

    def __unicode__(self):
        return self.title

class Item(models.Model):
    # Manager
    objects = ItemManager()

    # Status Fields
    public = models.BooleanField(_('Public'), default=True, help_text=_('Disable this Feed-Entry instead of deleting it'))

    # Feed-Item Details
    feed = models.ForeignKey(Feed, blank=False, null=False)
    guid = models.CharField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    url = models.URLField()
    summary = models.TextField()

    # Timestamps
    published = models.DateTimeField(auto_now_add=True)
    published_original = models.DateTimeField()

    class Meta:
        verbose_name = _('Item')
        verbose_name_plural = _('Items')
        ordering = ('-published',)

    def public_flag(self):
        return self.public
    public_flag.boolean = True
    public_flag.short_description = _('Public')

    def admin_action_checkbox(self):
        checkbox = '<input type="checkbox" name="item_id_list" value="%s""/>' % self.id
        return checkbox
    admin_action_checkbox.short_description = ''
    admin_action_checkbox.allow_tags = True

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/community/#%s' % escape(self.guid)
