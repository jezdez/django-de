import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings

from django_de.sitemaps import StaticFileSitemap
from django_de.apps.documentation.views import get_documents

static_urls = (
    '/',
    '/trac/',
    '/authors/',
    '/download/',
    '/imprint/',
    '/participate/',
    '/documentation/',
    # '/documentation/overview/',
    # '/documentation/install/',
    # '/documentation/tutorial01/',
    # '/documentation/faq/',
    # '/documentation/webdesign/',
    # '/documentation/shortcuts/',
    # '/documentation/settings/',
    # '/documentation/redirects/',
    # '/documentation/sites/',
    # '/documentation/api_stability/',
    # '/documentation/documentation/',
    # '/documentation/outputting_csv/',
    # '/documentation/add_ons/',
    # '/documentation/request_response/',
    # '/documentation/generic_views/',
    # '/documentation/url_dispatch/'
) + tuple(["/documentation/%s/" % document for document in get_documents()])

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
