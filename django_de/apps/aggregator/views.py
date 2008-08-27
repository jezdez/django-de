# -*- coding: utf-8 -*-

from django.db.models import get_model
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.template.defaultfilters import mark_safe
from django.utils.translation import ugettext as _
from django.core.mail import mail_admins
from django.views.generic.list_detail import object_list

from django_de.apps.aggregator.models import Feed, Item
from django_de.apps.aggregator.forms import NewFeedForm

def overview(request):
    params = {
        'queryset': Item.objects.latest_public(),
        'allow_empty': True,
        'template_object_name': 'item',
        'template_name': 'aggregator/overview.html',
        'extra_context': {
            'feed_list': Feed.objects.public().order_by('title'),
        },
    }
    return object_list(request, **params)

def add_feed(request):
    if request.POST:
        form = NewFeedForm(request.POST)
        if form.is_valid():
            form.save()
            message = _('A new feed has been added and awaits activation: %s') % form.cleaned_data.get('feed_url', '')
            mail_admins(_('Community: New feed added.'), message, True)
            return HttpResponseRedirect('/community/add/thankyou/')
    else:
        form = NewFeedForm()

    template_context = {
        'form': form,
        'feed_list': Feed.objects.public().order_by('title'),
    }

    return render_to_response(
        'aggregator/add_feed.html',
        template_context,
        RequestContext(request),
    )

def admin_actions(request, modelname, appname):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Superuser only!')

    model = get_model(modelname, appname)
    id_list = request.POST.getlist('item_id_list')

    if id_list:
        for id in id_list:
            obj = model.objects.get(pk=id)
            # Delete Item
            if request.POST.has_key('_delete'):
                obj.delete()
                request.user.message_set.create(message=_('"%s" was deleted') % mark_safe(obj.title))
            # Open Item
            elif request.POST.has_key('_markopen'):
                obj.public = True
                obj.save()
                request.user.message_set.create(message=_('"%s" was opened') % mark_safe(obj.title))
            # Close Item
            elif request.POST.has_key('_markclosed'):
                obj.public = False
                obj.save()
                request.user.message_set.create(message=_('"%s" was closed') % mark_safe(obj.title))
            # Wrong Action Parameter
            else:
                request.user.message_set.create(message='Wrong Action Parameter')
    # None Checkbox checked
    else:
        request.user.message_set.create(message=_('Nothing to do...'))

    return HttpResponseRedirect('/admin/%s/%s/' % (modelname, appname))
