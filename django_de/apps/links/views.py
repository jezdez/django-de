from datetime import datetime

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django import newforms as forms

from djangode.apps.links.models import Link, LANGUAGES
from djangode.apps.links.slughifi import slughifi
from tagging.forms import TagField

def add_link(request):
    class LinkForm(forms.Form):
        title = forms.CharField()
        url = forms.URLField()
        lang = forms.ChoiceField(choices = LANGUAGES)
        related_tags = TagField()
        comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))

    if request.method =='POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            link = Link()
            for field in ['title', 'url', 'lang', 'related_tags', 'comment']:
                setattr(link, field, data[field])
            link.slug = slughifi(link.title)
            link.submission_date = datetime.today()
            link.is_online = False
            link.save()

            return HttpResponseRedirect('/liens/')

    else:
        form = LinkForm()

    return render_to_response('links/link_form.html', { 'form': form })

