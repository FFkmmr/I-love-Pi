from django.core.management.base import BaseCommand
from pattern_finder.models import PiMil

CHUNK_SIZE = 1_000_000

class Command(BaseCommand):
    help = 'Load Pi chunks from file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the pi text file')

    def handle(self, *args, **options):
        file_path = options['file_path']
        with open(file_path, 'r', encoding='utf-8') as f:
            mil_number = 1
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                PiMil.objects.create(mil_number=mil_number, text=chunk)
                mil_number += 1
        self.stdout.write(self.style.SUCCESS('Loaded all chunks'))