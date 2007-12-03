from django.conf.urls.defaults import *
from djangode.apps.links.models import Link
from djangode.apps.links.views import add_link

urlpatterns = patterns('django.views.generic.date_based',
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'archive_month',
        dict(
            queryset = Link.published.all(),
            template_object_name = 'link',
            date_field='submission_date',
            month_format='%m',
        )
    ),
    (r'^(?P<year>\d{4})/$',
        'archive_year',
        dict(
            queryset = Link.published.all(),
            template_object_name = 'link',
            date_field='submission_date',
            make_object_list = True,
        )
    ),
    (r'^$',
        'archive_index',
        dict(
            queryset = Link.published.all(),
            date_field='submission_date',
            allow_empty=True,
        )
    ),
)

urlpatterns += patterns('', (r'^add/$', add_link))
