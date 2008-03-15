from django.conf.urls.defaults import *
from django_de.apps.authors.models import Author

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', 'object_list',
        dict(
            queryset = Author.objects.order_by('name', 'slug'),
            template_object_name = 'author',
            allow_empty=True,
        ),
    )
)
