import os

from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands import loaddata


class Command(BaseCommand):
    help = 'Loads all fixtures in the appropriate order'

    def _load_data(self, app, file):
        loaddata_command = loaddata.Command()
        file_path = os.path.join(app, 'fixtures', file)
        loaddata_command.run_from_argv(('./manage.py', 'loaddata', file_path))

    def handle(self, *args, **options):
        self._load_data('core', '0001_abilities.json')
        self._load_data('core', '0002_skills.json')
        self._load_data('core', '0003_dices.json')
