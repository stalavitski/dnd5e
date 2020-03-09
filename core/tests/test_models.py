from django.test import TestCase

from core.models import Dice, Feature, Skill, Source


class DiceTestCase(TestCase):
    fixtures = ('0003_dices.json',)

    def test__str__returns_correct_value(self):
        dice = Dice.objects.first()
        expected_result = 'd{}'.format(dice.sides)
        self.assertEqual(str(dice), expected_result)

    def test__roll__returns_number_in_range(self):
        dice = Dice.objects.first()

        for i in range(1, 100):
            roll = dice.roll()
            # Roll should be in the range [1, num of the Dice sides]
            self.assertLessEqual(roll, dice.sides)
            self.assertGreaterEqual(roll, 1)


class FeatureTestCase(TestCase):
    fixtures = ('0001_sources.json',)

    def test__str__returns_correct_value(self):
        source = Source.objects.first()
        feature = Feature.objects.create(name='Test', source=source)
        self.assertEqual(str(feature), feature.name)


class SkillTestCase(TestCase):
    fixtures = ('0002_skills.json',)

    def test__str__returns_correct_value(self):
        skill = Skill.objects.first()
        self.assertEqual(str(skill), skill.name)


class SourceTestCase(TestCase):
    fixtures = ('0001_sources.json',)

    def test__str__returns_correct_value(self):
        source = Source.objects.first()
        self.assertEqual(str(source), source.name)
