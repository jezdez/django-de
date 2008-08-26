from django.conf.urls.defaults import *
from django_de.apps.ticker import views as ticker_views
from django_de.apps.ticker.feeds import feeds

urlpatterns = patterns('',
    url(r'^$', ticker_views.overview, name='ticker_overview'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name='ticker_feeds'),

    url(r'^archive/$', ticker_views.archive, name='ticker_archive'),
    url(r'^archive/(?P<tag>.*)/$', ticker_views.archive_by_tag, name='ticker_archive_details'),
    
    # Details
    url(r'^(?P<id>[\d]+)-(?P<slug>[-\w]+)/$', ticker_views.details, name='ticker_details'),
)
