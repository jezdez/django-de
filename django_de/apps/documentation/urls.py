from django.conf.urls.defaults import *
from django_de.apps.documentation.views import index, detail

urlpatterns = patterns('',
    (r'^$', index),
    (r'^(?P<version>[\d.]+)/$', index),
    (r'^(?P<slug>[\w\.-]+)/$', detail),
    (r'^(?P<version>[\d.]+)/(?P<slug>[\w\.-]+)/$', detail),
)
