from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page

from django_de.apps.documentation.views import index, detail

cache_period = 60*60
urlpatterns = patterns('',
    (r'^$', cache_page(index, cache_period)),
    (r'^(?P<version>[\d.]+)/$', cache_page(index, cache_period)),
    (r'^(?P<slug>[\w\.-]+)/$', detail),
    (r'^(?P<version>[\d.]+)/(?P<slug>[\w\.-]+)/$', detail),
)
