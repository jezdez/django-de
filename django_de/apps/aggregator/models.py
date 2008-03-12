import re
from django.db import models
from django.conf import settings
from django.template.defaultfilters import striptags, escape
from django.utils.translation import ugettext as _
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
    
    class Admin:
        list_display = (
            'admin_action_checkbox',
            'public_flag',
            'title',
            'url_link',
            'errors',
            'keyword_check_flag',
            'keywords',
            'item_count',
            'published',
        )
        
        list_display_links = (
            'title',
        )
        
        list_filter = (
            'public',
            'published',
        )
        
        fields = (
            (_('Status'), {
                'fields': (
                    'public',
                ),
            }),            
            (_('Core Feed Data'), {
                'fields': (
                    'feed_url',
                    'url',
                    'title',
                    'owner_email',
                ),
            }),            
            (_('Keywords'), {
                'fields': (
                    'keyword_check',
                    'keywords',
                ),
            }),            
            (_('Debug'), {
                'fields': (
                    'errors',
                ),
            }),            
        )
    
    def admin_action_checkbox(self):        
        error = (self.errors >= settings.AGGREGATOR_MAX_ERRORS) and _('Broken!') or ''
        enabled = (self.errors >= settings.AGGREGATOR_MAX_ERRORS) and ' disabled="disabled"' or ''
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
        import md5
        from django.template.defaultfilters import escape
        return 'http://www.gravatar.com/avatar.php?gravatar_id=%s&default=%s&size=%s' % (
                md5.new(self.owner_email).hexdigest(),
                escape(settings.AGGREGATOR_GRAVATAR_DEFAULT_IMAGE),
                settings.AGGREGATOR_GRAVATAR_SIZE,
            )
    
    def __unicode__(self):
        return self.title
    
    
    
class Item(models.Model):
    
    # Manger
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
    
    class Admin: 
        list_display = (
            'admin_action_checkbox',
            'public_flag',
            'feed',
            'title',      
            'published',  
            'published_original',
        )
        
        list_display_links = (
            'title',
        )
    
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