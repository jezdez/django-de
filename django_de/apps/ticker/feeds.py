from django.contrib.syndication import feeds
from django.utils.feedgenerator import Atom1Feed

from django_de.apps.ticker.models import Entry

class LatestEntries(feeds.Feed):
    title = "django-de.org - Letzte News"
    link = "/"

    def items(self):
        return Entry.objects.public()[:30]
    
    def item_pubdate(self, item):
        return item.published

class LatestEntriesAtom(LatestEntries):
    feed_type = Atom1Feed

feeds = {
    'rss': LatestEntries,
    'atom': LatestEntriesAtom,
}
