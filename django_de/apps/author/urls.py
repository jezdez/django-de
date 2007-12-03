from django.conf.urls.defaults import *
from djangode.apps.authors.models import Contributor

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list',
        dict(
            queryset = Contributor.objects.all(),
            template_object_name = 'contributor',
            allow_empty=True,
        ),
    )
)