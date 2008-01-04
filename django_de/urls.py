import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings

from django_de.sitemaps import StaticFileSitemap

static_urls = (
    '/',
    '/trac/',
    '/authors/',
    '/download/',
    '/imprint/',
    '/participate/',
    '/documentation/',
    '/documentation/overview/',
    '/documentation/install/',
    '/documentation/webdesign/',
    '/documentation/shortcuts/',
    '/documentation/settings/',
    '/documentation/redirects/',
    '/documentation/tutorial01/',
)

sitemaps = {
    'static': StaticFileSitemap(static_urls, priority=0.5, changefreq='daily')
}

cache_period = 60*60
urlpatterns = patterns('',
    (r'^$', cache_page(direct_to_template, cache_period), {'template': 'homepage.html'}),
    (r'^download/', cache_page(direct_to_template, cache_period), {'template': 'download.html'}),
    (r'^imprint/', cache_page(direct_to_template, cache_period), {'template': 'impressum.html'}),
    (r'^participate/', cache_page(direct_to_template, cache_period), {'template': 'participate.html'}),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^documentation/', include('django_de.apps.documentation.urls')),
    (r'^authors/', include('django_de.apps.authors.urls')),
    (r'^sitemap.xml$', cache_page(sitemap, cache_period*6), {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/(?P<path>.*)$', 'serve', {
                'document_root': os.path.join(settings.PROJECT_PATH, 'site_media'),
                'show_indexes': True}),
        )
