from django.template.defaultfilters import dictsortreversed

from tagging.models import Tag
from collticker.models import Entry

def popular(request):

    latest_entries = Entry.objects.entries_by_user(request=request)

    poptags = Tag.objects.usage_for_model(Entry, counts=True, filters={'status': 'OPEN'})
    poptags = dictsortreversed(poptags, 'count')
    
    if len(poptags) < 1:
        poptags_max = 0
    else:
        poptags_max = poptags[0].count
    
    return {
        'popular_tags': poptags,
        'popular_tags_max': poptags_max,
        'latest_entries': latest_entries,
    }