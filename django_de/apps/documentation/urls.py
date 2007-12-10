from django.conf.urls.defaults import *

urlpatterns = patterns('django_de.apps.documentation.views',
    (r'^$', 'index'),
    (r'^(?P<version>[\d.]+)/$', 'index'),
    (r'^(?P<slug>[\w\.-]+)/$', 'detail'),
    (r'^(?P<version>[\d.]+)/(?P<slug>[\w\.-]+)/$', 'detail'),
)
