from django.core.management.base import NoArgsCommand

from django_de.apps.documentation.utils import get_absolute_document_urls
from django_de.apps.documentation.generator import quick_delete, StaticGeneratorException

class Command(NoArgsCommand):
    help = 'Used to autogenerate static files from SVN repository.'

    def handle_noargs(self, **options):
        try:
            quick_delete(get_absolute_document_urls())
        except StaticGeneratorException:
            pass
