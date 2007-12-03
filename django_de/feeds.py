#! -*- encoding: utf-8 -*-
from django.contrib.syndication.feeds import Feed
from django.utils.translation import ugettext_lazy as _

from djangode.apps.links.models import Link

class LatestLinks(Feed):
    title = _("latest links from django-de.org")
    link = "/liens/"
    description = u"Derniers liens ajoutés au site de Django-fr"

    def items(self, obj):
        return Link.published.order_by('-submission_date')[:5]
        
class LatestLinksPending(Feed):
    title = _("latest links from django-de.org (moderation)")
    link = "/links/"
    description = u"Derniers liens ajoutés au site de Django-fr"

    def items(self, obj):
        return Link.objects.order_by('-submission_date')[:5]
