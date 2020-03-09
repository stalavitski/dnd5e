from django.test import TestCase

from core.management.commands.populatedb import Command
from core.models import Dice, Skill, Source


class PopulateDBCommandTestCase(TestCase):
    def test__load_data__populates_db_with_fixture(self):
        populate_db = Command()
        skills_count = Skill.objects.count()
        self.assertEqual(skills_count, 0)
        populate_db._load_data('core', ('0002_skills.json',))
        skills_count = Skill.objects.count()
        self.assertGreater(skills_count, 0)

    def test__handle__populates_db_with_multiple_fixtures(self):
        populate_db = Command()
        sources_count = Source.objects.count()
        self.assertEqual(sources_count, 0)
        dices_count = Dice.objects.count()
        self.assertEqual(dices_count, 0)
        populate_db.handle()
        sources_count = Source.objects.count()
        self.assertGreater(sources_count, 0)
        dices_count = Dice.objects.count()
        self.assertGreater(dices_count, 0)
