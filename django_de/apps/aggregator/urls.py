from django.conf.urls.defaults import *
from django_de.apps.aggregator.feeds import feeds

urlpatterns = patterns('',
    # Die Community-Seite
    (r'^$', 'django_de.apps.aggregator.views.overview'),
    
    # Feed hinzufuegen
    (r'^add/$', 'django_de.apps.aggregator.views.add_feed'),
    (r'^add/thankyou/$', 'django.views.generic.simple.direct_to_template', {'template': 'aggregator/add_feed_thankyou.html'}),
    
    # Feed-Feed :-)
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    # Admin-Kram
    (r'^adminactions/(?P<modelname>[-\w]+)/(?P<appname>[-\w]+)/$', 'django_de.apps.aggregator.views.admin_actions'),     
)
