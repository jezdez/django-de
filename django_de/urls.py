from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page

cache_period = 60*60
urlpatterns = patterns('',
    (r'^$', cache_page(direct_to_template, cache_period), {'template': 'homepage.html'}),
    (r'^download/', cache_page(direct_to_template, cache_period), {'template': 'download.html'}),
    (r'^imprint/', cache_page(direct_to_template, cache_period), {'template': 'impressum.html'}),
    (r'^participate/', cache_page(direct_to_template, cache_period), {'template': 'participate.html'}),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^documentation/', include('django_de.apps.documentation.urls')),
    (r'^author/', include('django_de.apps.authors.urls')),
)

import os.path, settings
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/(?P<path>.*)$', 'serve', {
                'document_root': os.path.join(settings.PROJECT_PATH, 'site_media'),
                'show_indexes': True}),
        )