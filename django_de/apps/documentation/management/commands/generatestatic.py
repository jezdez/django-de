from django.core.management.base import NoArgsCommand

from django_de.apps.documentation.utils import get_documents

from django_de.apps.documentation.generator import quick_publish, StaticGeneratorException

class Command(NoArgsCommand):
    help = 'Used to autogenerate static files from SVN repository.'

    def handle_noargs(self, **options):
        try:
            quick_publish(get_documents())
        except StaticGeneratorException:
            pass
