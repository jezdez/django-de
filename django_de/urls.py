from django.conf.urls.defaults import *
import settings
import os.path

from tagging.models import Tag

urlpatterns = patterns('',
    (r'^admin/',         include('django.contrib.admin.urls')),
    (r'^documentation/', include('django_de.apps.documentation.urls')),
    (r'^author/', include('django_de.apps.authors.urls')),
)

urlpatterns += patterns('django.views.generic.list_detail',
    (r'^tags/(?P<slug>[^/]+)/(?u)$', 'object_detail',
        dict(
            queryset = Tag.objects.all(),
            template_object_name = 'tag',
            slug_field='name',
        )
    ),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'homepage.html'}),
    (r'^download/', 'direct_to_template', {'template': 'download.html'}),
    (r'^participate/', 'direct_to_template', {'template': 'participate.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/(?P<path>.*)$', 'serve', {
                'document_root': os.path.join(settings.PROJECT_PATH, 'site_media'),
                'show_indexes': True}),
        )