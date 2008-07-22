from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _

from django_de.apps.jobboard.manager import EntryManager

class Entry(models.Model):
    LOOKING_FOR_DEV = 1
    LOOKING_FOR_JOB = 2
    JOB_CHOICES = (
        (LOOKING_FOR_DEV, _('We are looking for (a) developer')),
        (LOOKING_FOR_JOB, _('I\'m looking for a job opportunity')),
    )
    # Manager
    objects = EntryManager()

    # Jobdaten
    job_type = models.IntegerField(max_length=1, choices=JOB_CHOICES)
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'))

    # Kontaktdaten
    name = models.CharField(_('Your name'), max_length=60)
    email = models.EmailField(_('Your email adress'))
    homepage = models.URLField(_('Your homepage'), blank=True)
    location = models.CharField(_('Your location'), max_length=60)

    # Datumsfelder
    published = models.DateTimeField(auto_now_add=True)
    published_until = models.DateField(blank=True, null=True)

    modified = models.DateTimeField(auto_now=True)
    modifier_ip_adress = models.IPAddressField()

    # Der geheime Edit-Key
    edit_key = models.CharField(max_length=40)

    # Boolean ob der Eintrag schon per E-Mail bestaetigt wurde
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Entry')
        verbose_name_plural = _('Entries')

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return ('django_de.apps.jobboard.views.details', [self.id])
    get_absolute_url = permalink(get_absolute_url)
