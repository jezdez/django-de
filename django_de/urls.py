import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.conf import settings

from django_de.sitemaps import StaticFileSitemap
from django_de.apps.documentation.utils import get_absolute_document_urls
from django_de.utils import cache_status

from django_de.apps.ticker.forms import BetterFreeThreadedCommentForm
from threadedcomments import views as tc_views


static_urls = (
    '/',
    '/trac/',
    '/authors/',
    '/download/',
    '/imprint/',
    '/participate/',
    '/documentation/',
) + get_absolute_document_urls()

sitemaps = {
    'static': StaticFileSitemap(static_urls, priority=0.5, changefreq='daily')
}

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'homepage.html'}),
    (r'^download/', direct_to_template, {'template': 'download.html'}),
    (r'^imprint/', direct_to_template, {'template': 'impressum.html'}),
    (r'^participate/', direct_to_template, {'template': 'participate.html'}),
    (r'^admin/(.*)', admin.site.root),
    (r'^documentation/', include('django_de.apps.documentation.urls')),
    (r'^news/', include('django_de.apps.ticker.urls')),
    (r'^community/', include('django_de.apps.aggregator.urls')),
    (r'^jobs/', include('django_de.apps.jobboard.urls')),
    (r'^cache_status/$', cache_status),
    (r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),
    (r'^robots.txt$', include('robots.urls')),

    # Overriding the default threadedcomment-form
    url(r'^threadedcomments/freecomment/(?P<content_type>\d+)/(?P<object_id>\d+)/$',
        tc_views.free_comment,
        {'form_class': BetterFreeThreadedCommentForm},
        name="tc_free_comment"),
    (r'^threadedcomments/', include('threadedcomments.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/(?P<path>.*)$', 'serve', {
                'document_root': os.path.join(settings.PROJECT_PATH, 'site_media'),
                'show_indexes': True}),
        )
