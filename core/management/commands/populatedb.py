import os

from django.core.management.base import BaseCommand
from django.core.management.commands import loaddata


class Command(BaseCommand):
    help = 'Loads fixtures in the appropriate order to populate database'

    def _load_data(self, app, files):
        loaddata_command = loaddata.Command()
        for file in files:
            file_path = os.path.join(app, 'fixtures', file)
            loaddata_command.run_from_argv(('./manage.py', 'loaddata', file_path))

    def handle(self, *args, **options):
        self._load_data('core', ('0001_sources.json', '0002_skills.json', '0003_dices.json'))
        self._load_data('characters', (
            '0001_levels.json',
            '0002_backgrounds.json',
            '0003_characters.json',
            '0004_character_abilities.json',
            '0005_character_skills.json'
        ))
