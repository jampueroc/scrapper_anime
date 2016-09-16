from django.core.management import BaseCommand

from visualizacion.scrapper import Scrapper


class Command(BaseCommand):
    help = 'This command search in an anime website and get information on a list, the alphabet to '
    def add_arguments(self, parser):
        parser.add_argument('--alphabet',
                            # nargs='*',
                            default='a-z',
                            type=str,
                            help='Scrapper works in range a-z')

    def handle(self, *args, **options):
        expresion = options['alphabet']
        error_urls = Scrapper.animes_urls(expresion,False)
        if len(error_urls) > 0:
            print "Urls with error"
            for urls in error_urls:
                print urls
