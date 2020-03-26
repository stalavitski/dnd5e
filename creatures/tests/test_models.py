from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import Condition, DamageType
from creatures.data import RESISTANCE_ADVANTAGE
from creatures.models import (
    Language,
    Race,
    RacialAbility,
    RacialFeature,
    RacialLanguage,
    RacialSkill,
    Script,
    Sense,RacialResistance,RacialSense,
    Size
)
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


class RacialFeatureTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0006_features.json',
        '0001_sizes.json',
        '0005_races.json',
        '0011_racial_features.json'
    )

    def test__str__returns_correct_value(self):
        racial_feature = RacialFeature.objects.select_related('feature', 'race').first()
        expected_value = 'Race: {}, Feature: {}'.format(racial_feature.race.name, racial_feature.feature.name)
        self.assertEqual(str(racial_feature), expected_value)


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


class RacialResistanceTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0004_damage_types.json',
        '0005_conditions.json',
        '0001_sizes.json',
        '0005_races.json',
        '0010_racial_resistances.json'
    )

    def test__str__returns_correct_value(self):
        racial_resistance = RacialResistance.objects.select_related('condition', 'damage_type', 'race').first()
        resistance_from = (racial_resistance.damage_type.name if racial_resistance.damage_type
                           else racial_resistance.condition.name)
        expected_value = 'Race: {}, Resistance: {} {}'.format(
            racial_resistance.race.name,
            resistance_from,
            racial_resistance.type
        )
        self.assertEqual(str(racial_resistance), expected_value)

    # save tests
    def test__save__raises_exception_on_create__when_condition_and_damage_type_are_not_set(self):
        race = Race.objects.first()
        with self.assertRaises(ValidationError) as cm:
            RacialResistance.objects.create(race=race, type=RESISTANCE_ADVANTAGE)
        error_message = cm.exception.messages.pop()
        self.assertEqual(error_message, RacialResistance.VALIDATION_ERROR_NO_FK)

    def test__save__raises_exception_on_create__when_condition_and_damage_type_are_both_set(self):
        condition = Condition.objects.first()
        damage_type = DamageType.objects.first()
        race = Race.objects.first()
        with self.assertRaises(ValidationError) as cm:
            RacialResistance.objects.create(
                condition=condition,
                damage_type=damage_type,
                race=race,
                type=RESISTANCE_ADVANTAGE
            )
        error_message = cm.exception.messages.pop()
        self.assertEqual(error_message, RacialResistance.VALIDATION_ERROR_BOTH_FK)

    def test__save__successfully_creates_instance_on_create__when_condition_is_set(self):
        condition = Condition.objects.first()
        race = Race.objects.first()
        racial_resistance = RacialResistance.objects.create(
            condition=condition,
            race=race,
            type=RESISTANCE_ADVANTAGE
        )
        self.assertIsNotNone(racial_resistance.id)

    def test__save__successfully_creates_instance_on_create__when_damage_type_is_set(self):
        damage_type = DamageType.objects.first()
        race = Race.objects.first()
        racial_resistance = RacialResistance.objects.create(
            damage_type=damage_type,
            race=race,
            type=RESISTANCE_ADVANTAGE
        )
        self.assertIsNotNone(racial_resistance.id)


class RacialSenseTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0001_sizes.json',
        '0004_senses.json',
        '0005_races.json',
        '0009_racial_senses.json'
    )

    def test__str__returns_correct_value(self):
        racial_sense = RacialSense.objects.select_related('race', 'sense').first()
        expected_value = 'Race: {}, Sense: {} {}'.format(
            racial_sense.race.name,
            racial_sense.sense.name,
            racial_sense.value
        )
        self.assertEqual(str(racial_sense), expected_value)


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
