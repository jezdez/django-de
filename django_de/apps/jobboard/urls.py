from django.conf.urls.defaults import *

urlpatterns = patterns('django_de.apps.jobboard.views',
    # Die Community-Seite
    (r'^$', 'overview'),
    (r'^add/$', 'add'),
    (r'^thankyou/$', 'thankyou'),
    (r'^(?P<jobid>[\d]+)/$', 'details'),
    (r'^edit/(?P<jobid>[\d]+)-(?P<key>[a-z0-9]{40})/$', 'edit'),
    (r'^verify/(?P<jobid>[\d]+)-(?P<key>[a-f0-9]{40})/$', 'verify'),
)
