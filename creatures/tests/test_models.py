from django.test import TestCase

from creatures.models import Language, Race, RacialAbility, RacialLanguage, RacialSkill, Script, Sense, Size
from creatures.utils import get_proficiency_verbose


class LanguageTestCase(TestCase):
    fixtures = (
        '0002_scripts.json',
        '0003_languages.json'
    )

    def test__str__returns_correct_value(self):
        language = Language.objects.first()
        self.assertEqual(str(language), language.name)


class RaceTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0001_sizes.json',
        '0005_races.json'
    )

    def test__str__returns_correct_value(self):
        race = Race.objects.first()
        self.assertEqual(str(race), race.name)


class RacialAbilityTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0001_sizes.json',
        '0005_races.json',
        '0007_racial_abilities.json'
    )

    def test__str__returns_correct_value(self):
        racial_ability = RacialAbility.objects.select_related('race').first()
        expected_value = 'Race: {}, Ability Score Increase: {} {}'.format(
            racial_ability.race.name,
            racial_ability.ability,
            racial_ability.value
        )
        self.assertEqual(str(racial_ability), expected_value)


class RacialLanguageTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0001_sizes.json',
        '0002_scripts.json',
        '0003_languages.json',
        '0005_races.json',
        '0006_racial_languages.json'
    )

    def test__str__returns_correct_value(self):
        racial_language = RacialLanguage.objects.select_related('language', 'race').first()
        expected_value = 'Race: {}, Language: {}'.format(racial_language.race.name, racial_language.language.name)
        self.assertEqual(str(racial_language), expected_value)


class RacialSkillTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0001_sizes.json',
        '0005_races.json',
        '0002_skills.json',
        '0008_racial_skills.json'
    )

    def test__str__returns_correct_value(self):
        racial_skill = RacialSkill.objects.select_related('race', 'skill').first()
        expected_value = 'Race: {}, Skill Proficiency: {} {}'.format(
            racial_skill.race.name,
            racial_skill.skill.name,
            get_proficiency_verbose(racial_skill.proficiency)
        )
        self.assertEqual(str(racial_skill), expected_value)


class ScriptTestCase(TestCase):
    fixtures = (
        '0002_scripts.json',
    )

    def test__str__returns_correct_value(self):
        script = Script.objects.first()
        self.assertEqual(str(script), script.name)


class SenseTestCase(TestCase):
    fixtures = (
        '0004_senses.json',
    )

    def test__str__returns_correct_value(self):
        sense = Sense.objects.first()
        self.assertEqual(str(sense), sense.name)


class SizeTestCase(TestCase):
    fixtures = (
        '0001_sizes.json',
    )

    def test__str__returns_correct_value(self):
        size = Size.objects.first()
        self.assertEqual(str(size), size.name)
