import os

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads fixtures in the appropriate order to populate database'

    def _load_data(self, app, files):
        for file in files:
            file_path = os.path.join(app, 'fixtures', file)
            call_command('loaddata', file_path)

    def handle(self, *args, **options):
        self._load_data('users', ('0001_users.json',))
        self._load_data('core', (
            '0001_sources.json',
            '0002_skills.json',
            '0003_dices.json',
            '0004_damage_types.json',
            '0005_conditions.json',
            '0006_features.json'
        ))
        self._load_data('creatures', (
            '0001_sizes.json',
            '0002_scripts.json',
            '0003_languages.json',
            '0004_senses.json',
            '0005_races.json',
            '0006_racial_languages.json',
            '0007_racial_abilities.json',
            '0008_racial_skills.json',
            '0009_racial_senses.json',
            '0010_racial_resistances.json',
            '0011_racial_features.json'
        ))
        self._load_data('characters', (
            '0001_levels.json',
            '0002_backgrounds.json',
            '0003_characters.json',
            '0004_character_abilities.json',
            '0005_character_skills.json',
            '0006_character_saving_throws.json'
        ))
