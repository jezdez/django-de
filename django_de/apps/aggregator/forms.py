# -*- coding: utf-8 -*-

import feedparser
from django import forms
from django_de.apps.aggregator.models import Feed

class NewFeedForm(forms.ModelForm):
    feed_url = forms.URLField(
        label = 'Die Adresse deines Feeds:',
    )

    url = forms.URLField(
        label = 'Die Adresse deines Weblogs oder deiner Homepage:',
    )

    title = forms.CharField(
        label = 'Der Titel deines Weblogs oder dein Name:',
    )

    owner_email = forms.EmailField(
        label = 'Deine E-Mail-Adresse',
        help_text='Die E-Mail dient nur zur Kontaktaufnahme im Falle von Problemen und wird für den Gravatar verwendet. Sie wird nicht öffentlich angezeigt!'
    )

    def clean_feed_url(self):
        feed_url = self.cleaned_data.get('feed_url', '')
        parsed_feed = feedparser.parse(feed_url)

        if not parsed_feed.version:
            raise forms.ValidationError('Das ist kein Feed. Bitte prüfe, ob der Feed valide ist.')
        return feed_url

    class Meta:
        model = Feed
        fields = (
            'feed_url',
            'url',
            'title',
            'owner_email',
        )
