# -*- coding: utf-8 -*-

from django.core.mail import mail_admins
import tagging

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth.decorators import permission_required
from django.utils.translation import gettext_lazy as _

from comments.forms import AntibotCommentForm
from collticker.models import Entry
from collticker.forms import NewPublicEntryForm
from tagging.models import Tag, TaggedItem


def overview(request, page=None, per_page=10, template_name='weblog/index.html'):
    '''The Index page of the weblog'''

    entry_list = Entry.objects.entries_by_user(request=request)

    template_context = {
        'entry_list': entry_list,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )

def archive(request, template_name='weblog/archive.html'):
    
    entry_list = Entry.objects.entries_by_user(request=request)
    tag_list = Tag.objects.cloud_for_model(Entry, steps=9, filters={'status': 'OPEN'})
        
    template_context = {
        'entry_list': entry_list,
        'tag_list': tag_list,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )

def archive_by_tag(request, tag, template_name='weblog/archive_by_tag.html'):

    entry_list = TaggedItem.objects.get_by_model(Entry.objects.entries_by_user(request=request), [tag])
    related_tags = Tag.objects.related_for_model([tag], Entry)

    template_context = {
        'the_tag': tag,
        'related_tags': related_tags,
        'entry_list': entry_list,
    }

    return render_to_response(
        template_name,
        template_context,
        context_instance=RequestContext(request)
    )


def details(request, id, slug, template_name='weblog/details.html'):

    entry = get_object_or_404(Entry.objects.entries_by_user(request=request), pk=id)

    if request.method == 'POST':
        form = AntibotCommentForm(request.POST)
        if form.is_valid():
            form.save(
                ip_address = request.META['REMOTE_ADDR'],
                content_object = entry,
                user_object = request.user,
            )
            return HttpResponseRedirect("%s#comments" % entry.get_absolute_url())
    else:
        form = AntibotCommentForm()

    template_context = {
        'entry': entry,
        'comment_form': form,
        'is_detail': True,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )


#===============================================================================
# Interaction
#===============================================================================

@permission_required('collticker.change_status')
def set_status(request, id, slug, status):
    entry = get_object_or_404(Entry.objects.entries_by_user(request=request), pk=id)
    entry.status = str(status).upper()
    entry.save()
    return HttpResponseRedirect(entry.get_absolute_url())


@permission_required('collticker.add_entry')
def add_entry(request, template_name="weblog/add_entry.html"):

    publish_instantly = request.user.has_perm('collticker.publish_instantly')

    if request.method == 'POST':
        entry_form = NewPublicEntryForm(request.POST)
        if entry_form.is_valid():
            new_entry = entry_form.save(commit=False)
            new_entry.author = request.user
            new_entry.status = publish_instantly and "OPEN" or "DRAFT"
            new_entry.save()

            # TODO: Anständige E-Mail senden
            mail_admins('New entry', 'new entry on djangohq', fail_silently=False)

            if publish_instantly:
                return HttpResponseRedirect(new_entry.get_absolute_url())
            else:
                thankyou = new_entry.get_absolute_url()+'#danke'
                return HttpResponseRedirect(thankyou)
    else:
        entry_form = NewPublicEntryForm()

    template_context = {
        'entry_form': entry_form,
        'taglist': tagging.models.Tag.objects.all(),
        'publish_instantly': publish_instantly,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )

@permission_required('collticker.change_entry')
def edit_entry(request, id, slug, template_name="weblog/add_entry.html"):

    entry = get_object_or_404(Entry.objects.entries_by_user(request=request), pk=id)

    if request.method == 'POST':
        entry_form = NewPublicEntryForm(request.POST, instance=entry)
        if entry_form.is_valid():
            new_entry = entry_form.save()
            return HttpResponseRedirect(new_entry.get_absolute_url())
    else:
        entry_form = NewPublicEntryForm(instance=entry)

    template_context = {
        'entry': entry,
        'entry_form': entry_form,
        'taglist': tagging.models.Tag.objects.all(),
        'is_edit': True,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )