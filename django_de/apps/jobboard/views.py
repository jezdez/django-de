import sha
import random
import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.template import loader
from django.http import HttpResponseRedirect, Http404
from django.core.mail import send_mail, mail_admins
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django_de.apps.jobboard.models import Entry
from django_de.apps.jobboard.forms import JobEntryForm

def overview(request):
    template_context = {
        'jobs': Entry.objects.get_jobs(),
        'developers': Entry.objects.get_developer(),
    }

    return render_to_response('jobboard/overview.html',
        template_context, RequestContext(request),
    )

def add(request):
    if request.POST:
        form = JobEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.modifier_ip_adress = request.META.get('REMOTE_ADDR')
            entry.edit_key = sha.new(str(random.random())).hexdigest()
            entry.save()

            # Mail an den Besitzer um den Beitrag freischalten zu lassen
            add_message = loader.render_to_string('jobboard/mail/add_notify.txt', {'entry': entry})
            send_mail(
                'Deine Stellenanzeige bei django-de.org',
                add_message,
                settings.DEFAULT_FROM_EMAIL,
                (entry.email,)
            )
            mail_admins(
                _('New job offer or application'),
                add_message,
                True
            )
            # Zur Danke-Seite weiterleiten
            return HttpResponseRedirect('/jobs/thankyou/')
    else:
        form = JobEntryForm()

    template_context = {
        'form': form,
    }
    return render_to_response('jobboard/add.html',
        template_context, RequestContext(request),
    )

def edit(request, jobid, key):
    try:
        entry = Entry.objects.get(id=int(jobid), edit_key=key)
    except Entry.DoesNotExist:
        raise Http404(_('This job offer or application doesn\'t exist (anymore)'))
    
    if request.POST:
        
        # Eintrag loeschen
        if request.POST.has_key('delete'):
            entry.delete()
            return HttpResponseRedirect('/jobs/?deleted=ok')

        # Eintrag aendern
        form = JobEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.modifier_ip_adress = request.META.get('REMOTE_ADDR')
            entry.save()
            return HttpResponseRedirect(entry.get_absolute_url())
    else:
        form = JobEntryForm(instance=entry)

    template_context = {
        'form': form,
        'is_edit_form': True,
    }
    return render_to_response('jobboard/add.html',
        template_context, RequestContext(request),
    )

def verify(request, jobid, key):
    try:
        entry = Entry.objects.get(id=int(jobid), edit_key=key)
    except Entry.DoesNotExist:
        raise Http404(_('This job offer or application doesn\'t exist (anymore)'))
    
    entry.verified = True
    entry.save()

    template_context = {
        'jobentry': entry,
    }
    return render_to_response('jobboard/details_verified.html',
        template_context, RequestContext(request),
    )

def details(request, jobid):
    template_context = {
        'jobentry': get_object_or_404(Entry, pk=jobid)
    }

    return render_to_response('jobboard/details.html',
        template_context, RequestContext(request),
    )

def thankyou(request):
    return render_to_response('jobboard/thankyou.html',
        {}, RequestContext(request),
    )
