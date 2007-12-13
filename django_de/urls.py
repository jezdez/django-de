import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import GenericSitemap
from django.conf import settings

from django_de.apps.documentation.models import Documentation
from django_de.apps.authors.models import Author
from django_de.sitemaps import StaticFileSitemap

doc_dict = {
    'queryset': Documentation.objects.all(),
}

author_dict = {
    'queryset': Author.objects.all(),
}

static_urls = (
    '/',
    '/download/',
    '/imprint/',
    '/participate/',
)

sitemaps = {
    'documentation': GenericSitemap(doc_dict, priority=0.6),
    'authors': GenericSitemap(author_dict, priority=0.6),
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
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/(?P<path>.*)$', 'serve', {
                'document_root': os.path.join(settings.PROJECT_PATH, 'site_media'),
                'show_indexes': True}),
        )
