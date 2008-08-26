# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from django_de.apps.ticker.models import Entry
from tagging.models import Tag, TaggedItem


def overview(request, page=None, per_page=10, template_name='ticker/overview.html'):
    '''The Index page of the ticker'''

    entry_list = Entry.objects.public()

    template_context = {
        'entry_list': entry_list,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )

def archive(request, template_name='ticker/archive.html'):
    
    entry_list = Entry.objects.public()
    tag_list = Tag.objects.cloud_for_model(Entry, steps=9, filters={'status': Entry.STATUS_OPEN})
        
    template_context = {
        'entry_list': entry_list,
        'tag_list': tag_list,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )

def archive_by_tag(request, tag, template_name='ticker/archive_by_tag.html'):

    entry_list = TaggedItem.objects.get_by_model(Entry.objects.public(), [tag])
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


def details(request, id, slug, template_name='ticker/details.html'):
    entry = get_object_or_404(Entry.objects.public(), pk=id)
    template_context = {
        'entry': entry,
        'is_detail': True,
    }

    return render_to_response(
        template_name,
        template_context,
        RequestContext(request),
    )
