from django.contrib.syndication.feeds import Feed
from django_de.apps.aggregator.models import Item

class LatestItems(Feed):
    title = "django-de.org Community Aggregator"
    link = "/community/"

    def items(self):
        return Item.objects.latest_public()[:30]
        
    def item_pubdate(self, item):
        return item.published_original
    
    def item_link(self, item):
        return item.url
    
    def item_author_name(self, item):
        return item.feed.title
    
    def item_author_link(self, item):
        return item.feed.url
            
feeds = {
    'latest': LatestItems,
}