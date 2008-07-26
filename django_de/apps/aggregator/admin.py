from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_de.apps.aggregator.models import Feed, Item

class FeedAdmin(admin.ModelAdmin):
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


class ItemAdmin(admin.ModelAdmin):
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

admin.site.register(Feed, FeedAdmin)
admin.site.register(Item, ItemAdmin)