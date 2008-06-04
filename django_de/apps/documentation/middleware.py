import re
from django.conf import settings
from staticgenerator import StaticGenerator

from django_de.apps.documentation.utils import get_absolute_document_urls

class StaticGeneratorMiddleware(object):
    urls = tuple([re.compile(r'^%s' % url) for url in get_absolute_document_urls()])
    
    def process_response(self, request, response):
        if response.status_code == 200:
            for url in self.urls:
                if url.match(request.path):
                    gen = StaticGenerator()
                    gen.publish_from_path(request.path, response.content)
                    break
        return response
