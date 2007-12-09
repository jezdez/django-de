from django.conf.urls.defaults import *

urlpatterns = patterns('django_de.apps.documentation.views',
    (r'^$', 'doc_index'),
    (r'^(?P<version>[\d.]+)/$', 'doc_index'),
    (r'^(?P<slug>[\w\.-]+)/$', 'doc_detail'),
    (r'^(?P<version>[\d.]+)/(?P<slug>[\w\.-]+)/$', 'doc_detail'),
)
