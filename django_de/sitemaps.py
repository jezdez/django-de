from django.contrib.sitemaps import Sitemap

class StaticFilePage:
    "Custom Page class for use with static template in sitemaps"
    def __init__(self, url):
        self.url = url
    def get_absolute_url(self):
        return self.url
        
class StaticFileSitemap(Sitemap):
    "Custom Sitemap Class for use with static templates"
    def __init__(self, urls, priority=0.5, changefreq='daily'):
        self.priority = priority
        self.changefreq = changefreq
        self.item_list = []
        if type(urls) not in (list, tuple):
            urls = [urls]
        for url in urls:
            self.item_list.append(StaticFilePage(url))
    
    def items(self):
        return self.item_list
