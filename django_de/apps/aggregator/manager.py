from django.db import models

class FeedManager(models.Manager):
    def public(self):
        return self.filter(public=True)

class ItemManager(models.Manager):
    def latest_public(self):
        return self.filter(public=True).select_related().order_by('-published_original')
