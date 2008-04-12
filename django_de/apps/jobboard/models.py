from django.db import models
from django_de.apps.jobboard.manager import EntryManager

JOB_CHOICES = (
    (1, 'Wir suchen (einen) Entwickler'),
    (2, 'Ich bin Entwickler und suche nach Herausforderungen'), #FIXME: Das klingt doof
)

class Entry(models.Model):

    # Manager
    objects = EntryManager()

    # Jobdaten
    job_type = models.IntegerField(max_length=1, choices=JOB_CHOICES)
    title = models.CharField('Titel', max_length=100)
    description = models.TextField('Beschreibung')

    # Kontaktdaten
    name = models.CharField('Dein Name', max_length=60)
    email = models.EmailField('Deine E-Mail-Adresse')
    homepage = models.URLField('Homapge', blank=True)
    location = models.CharField('Wohnort', max_length=60)

    # Datumsfelder
    published = models.DateTimeField(auto_now_add=True)
    published_until = models.DateField(blank=True, null=True)

    modified = models.DateTimeField(auto_now=True)
    modifier_ip_adress = models.IPAddressField()

    # Der geheime Edit-Key
    edit_key = models.CharField(max_length=40)

    # Boolean ob der Eintrag schon per E-Mail bestaetigt wurde
    verified = models.BooleanField(default=False)

    class Admin:
        list_display = (
            'name',
            'job_type',
            'verified',
            'published',
        )

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return '/jobs/%s/' % self.id
