from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = "Runs server. If parameters are passed it runs commands: mm -> makemigrations, m -> migrate,\
            csu -> createsuperuser, ir -> install requirements, t -> test."

    def add_arguments(self, parser):
        parser.add_argument('-arg', '--arguments', type=str, nargs='*')

    def handle(self, *args, **options):
        arguments = options['arguments']
        try:
            if 'mm' in arguments:
                call_command('makemigrations')
            if 'm' in arguments:
                call_command('migrate')
            if 'csu' in arguments:
                call_command('createsuperuser')
            if 't' in arguments:
                call_command('test')
            if 'ir' in arguments:
                os.system('pip install -r requirements.txt')
        except TypeError:
            call_command('runserver', '127.0.0.1:7373')
