# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from threadedcomments.forms import FreeThreadedCommentForm

class BetterFreeThreadedCommentForm(FreeThreadedCommentForm):

    def __init__(self, *args, **kwargs):
        super(BetterFreeThreadedCommentForm, self).__init__(*args, **kwargs)

        # Felder verstecken
        self.fields['markup'].widget = forms.HiddenInput()
        self.fields['email'].widget = forms.HiddenInput(attrs={'autocomplete': 'off'})

        # Labels eindeutschen
        self.fields['name'].label = u'Dein Name'
        self.fields['website'].label = u'Homepage'
        self.fields['comment'].label = u'Kommentar'

    def clean_email(self):
        '''
        Honeypot-Feld als HiddenInput.
        Gibt eine Fehlermeldung aus, *wenn* eine E-Mail eingetragen wurde.
        '''
        if self.cleaned_data.get('email', False):
            raise forms.ValidationError(u'Wir möchten deine E-Mail-Adresse NICHT wissen, bitte ' \
                                         'lasse dieses Feld leer!')
        return self.cleaned_data.get('email')

    def clean_name(self):
        '''
        Simples Keyword-Blocking. Gesperrte Usernamen werden in einer Tupel in
        settings.THREADEDCOMMENTS_BLOCKED_USERNAMES definiert.
        '''
        this_name = self.cleaned_data.get('name')
        for blocked_name in getattr(settings, 'THREADEDCOMMENTS_BLOCKED_USERNAMES', ()):
            if blocked_name in this_name:
                raise forms.ValidationError(u'Dein Name enthält ein gesperrtes Wort: "%s". Bitte entferne '\
                                             'es aus deinem Namen.' % blocked_name)
        return this_name

