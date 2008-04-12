from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Die Community-Seite
    (r'^$', 'django_de.apps.jobboard.views.overview'),
    (r'^add/$', 'django_de.apps.jobboard.views.add'),
    (r'^(?P<jobid>[\d]+)/$', 'django_de.apps.jobboard.views.details'),
    (r'^edit/(?P<jobid>[\d]+)-(?P<key>[a-z0-9]{40})/$', 'django_de.apps.jobboard.views.edit'),
    (r'^verify/(?P<jobid>[\d]+)-(?P<key>[a-f0-9]{40})/$', 'django_de.apps.jobboard.views.verify'),
)