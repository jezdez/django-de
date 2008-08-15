# -*- coding: utf-8 -*-

from django import forms
from django_de.apps.jobboard.models import Entry

import datetime
from django import forms

class JobEntryForm(forms.ModelForm):

    job_type = forms.ChoiceField(
        label = 'Stellenangebot oder -gesuch aufgeben?',
        choices = Entry.JOB_CHOICES,
    )

    description = forms.CharField(
        label = 'Beschreibung',
        widget = forms.Textarea,
        max_length = 5000,
        min_length = 60,
    )

    location = forms.CharField(
        label = 'Dein Wohnort oder Ort des Abeitsplatzes'
    )

    homepage = forms.URLField(
        required = False,
        label = 'Homepage: (optional)',
    )

    published_until = forms.DateField(
        required = False,
        widget = forms.TextInput(attrs={'class': 'datum'}),
        label = u'Anzeigen bis: (optional)',
        help_text = 'Lasse dieses Feld leer, um das Inserat für immer anzeigen zu \
                     lassen.<br/>Ansonsten gib das Datum im Format YYYY-MM-DD an.',
        # TODO: Hier ein Dropdown-Widget nutzen? Wie dann aber
        #       unendlich lange Anzeigen markieren?
    )

    class Meta:
        model = Entry
        fields = (
            'job_type',
            'title',
            'description',

            'name',
            'email',
            'homepage',
            'location',

            'published_until',
        )