from django.core.management.base import NoArgsCommand
from optparse import make_option

from django_de.apps.documentation.models import get_documents
from django_de.generator import StaticGenerator, StaticGeneratorException

class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--repo', dest='repo', default=None,
            help='The repository path.'),
        make_option('--rev', dest='rev', default=None,
            help='The revision number.'),
    )
    help = 'Used to autogenerate static files from SVN repository.'

    def handle_noargs(self, **options):
        repo = options.get('repo', None)
        rev = options.get('rev', None)

        try:
            for document in get_documents():
                gen = StaticGenerator((document,))
                gen.start()
        except StaticGeneratorException:
            pass
