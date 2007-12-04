from django.conf.urls.defaults import *
from django_de.apps.documentation.models import Documentation

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^(?P<slug>[-\w]+)/$', 'object_detail',
        dict(
            queryset = Documentation.objects.all(),
            template_object_name = 'documentation',
            slug_field='slug',
        )
    ),
    (r'^$', 'object_list',
        dict(
            queryset = Documentation.objects.all(),
            template_object_name = 'documentation',
            allow_empty=True,
        ),
    )
)