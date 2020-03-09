from django.test import TestCase

from characters.data import PROFICIENCY_EXP, PROFICIENCY_PROF
from characters.models import (
    Background,
    Character,
    CharacterAbility,
    CharacterSavingThrow,
    CharacterSkill,
    Class,
    Level
)
from core.data import ABILITY_DEXTERITY, ABILITY_DICT
from core.models import Skill


class BackgroundTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0002_backgrounds.json'
    )

    def test__str__returns_correct_value(self):
        background = Background.objects.first()
        self.assertEqual(str(background), background.name)


class CharacterTestCase(TestCase):
    fixtures = (
        '0001_users',
        '0001_sources.json',
        '0002_skills.json',
        '0001_levels.json',
        '0002_backgrounds.json',
        '0003_characters.json',
        '0004_character_abilities.json'
    )

    def test__str__returns_correct_value(self):
        character = Character.objects.first()
        self.assertEqual(str(character), character.name)

    def test__initiative__returns_correct_value(self):
        character = Character.objects.first()
        character_dexterity = character.character_abilities.get(ability=ABILITY_DEXTERITY)
        values_map = {
            7: -2,
            8: -1,
            10: 0,
            12: 1,
            13: 1
        }

        for dexterity, initiative in values_map.items():
            character_dexterity.value = dexterity
            character_dexterity.save()
            self.assertEqual(character.initiative, initiative)
            # Invalidate cache of cached_property
            del character.initiative

    def test__level__returns_correct_object(self):
        character = Character.objects.first()
        values_map = {
            0: 1,
            299: 1,
            300: 2,
            300000: 18,
            355000: 20
        }

        for experience, level in values_map.items():
            character.experience = experience
            character.save()
            self.assertEqual(character.level.value, level)
            # Invalidate cache of cached_property
            del character.level

    def test__save__creates_default_relations__when_record_is_added(self):
        background = Background.objects.first()
        character = Character(background=background, name='Test')
        self.assertTrue(character._state.adding)
        character.save()
        # Abilities are created
        self.assertEqual(character.character_abilities.count(), len(ABILITY_DICT))
        # Skills are created
        skills_count = Skill.objects.count()
        self.assertEqual(character.character_skills.count(), skills_count)
        # Details is created
        self.assertIsNotNone(character.details)


class CharacterAbilityTestCase(TestCase):
    fixtures = (
        '0001_users.json',
        '0001_sources.json',
        '0001_levels.json',
        '0002_backgrounds.json',
        '0003_characters.json',
        '0004_character_abilities.json'
    )

    def test__str__returns_correct_value(self):
        character_ability = CharacterAbility.objects.first()
        expected_value = '{} Ability'.format(character_ability.ability_name)
        self.assertEqual(str(character_ability), expected_value)

    def test__ability_name__returns_correct_value(self):
        character_ability = CharacterAbility.objects.first()
        ability_name = ABILITY_DICT.get(character_ability.ability)
        self.assertEqual(character_ability.ability_name, ability_name)

    def test__modifier__returns_correct_value(self):
        character_ability = CharacterAbility.objects.first()
        values_map = {
            7: -2,
            8: -1,
            10: 0,
            12: 1,
            13: 1
        }

        for value, modifier in values_map.items():
            character_ability.value = value
            self.assertEqual(character_ability.modifier, modifier)


class CharacterSavingThrowTestCase(TestCase):
    fixtures = (
        '0001_users',
        '0001_sources.json',
        '0001_levels.json',
        '0002_backgrounds.json',
        '0003_characters.json',
        '0004_character_abilities.json',
        '0006_character_saving_throws.json'
    )

    def test__str__returns_correct_value(self):
        character_saving_throw = CharacterSavingThrow.objects.first()
        expected_value = '{} Saving Throw'.format(character_saving_throw.ability_name)
        self.assertEqual(str(character_saving_throw), expected_value)

    def test__ability_name__returns_correct_value(self):
        character_saving_throw = CharacterSavingThrow.objects.first()
        ability_name = ABILITY_DICT.get(character_saving_throw.ability)
        self.assertEqual(character_saving_throw.ability_name, ability_name)

    # modifier tests
    def test__modifier__returns_correct_value__if__not_proficient(self):
        character_saving_throw = CharacterSavingThrow.objects.select_related('character').first()
        modifier = CharacterAbility.objects.get(
            ability=character_saving_throw.ability,
            character=character_saving_throw.character
        ).modifier
        self.assertEqual(character_saving_throw.modifier, modifier)

    def test__modifier__returns_correct_value__if_proficient(self):
        character_saving_throw = CharacterSavingThrow.objects.select_related('character').first()
        character_saving_throw.is_proficient = True
        proficiency_bonus = character_saving_throw.character.level.proficiency_bonus
        ability_modifier = CharacterAbility.objects.get(
            ability=character_saving_throw.ability,
            character=character_saving_throw.character
        ).modifier
        modifier = proficiency_bonus + ability_modifier
        self.assertEqual(character_saving_throw.modifier, modifier)


class CharacterSkillTestCase(TestCase):
    fixtures = (
        '0001_users',
        '0001_sources.json',
        '0002_skills.json',
        '0001_levels.json',
        '0002_backgrounds.json',
        '0003_characters.json',
        '0004_character_abilities.json',
        '0005_character_skills.json'
    )

    def test__str__returns_correct_value(self):
        character_skill = CharacterSkill.objects.select_related('skill').first()
        expected_value = character_skill.skill.name + ' Skill'
        self.assertEqual(str(character_skill), expected_value)

    # modifier tests
    def test__modifier__returns_correct_value__if_not_proficient(self):
        character_skill = CharacterSkill.objects.select_related('character', 'skill').first()
        modifier = CharacterAbility.objects.get(
            ability=character_skill.skill.ability,
            character=character_skill.character
        ).modifier
        self.assertEqual(character_skill.modifier, modifier)

    def test__modifier__returns_correct_value__if_proficient(self):
        character_skill = CharacterSkill.objects.select_related('character', 'skill').first()
        character_skill.proficiency = PROFICIENCY_PROF
        modifier = CharacterAbility.objects.get(
            ability=character_skill.skill.ability,
            character=character_skill.character
        ).modifier
        proficiency_bonus = character_skill.character.level.proficiency_bonus
        modifier += proficiency_bonus
        self.assertEqual(character_skill.modifier, modifier)

    def test__modifier__returns_correct_value__if_expert(self):
        character_skill = CharacterSkill.objects.select_related('character', 'skill').first()
        character_skill.proficiency = PROFICIENCY_EXP
        modifier = CharacterAbility.objects.get(
            ability=character_skill.skill.ability,
            character=character_skill.character
        ).modifier
        proficiency_bonus = character_skill.character.level.proficiency_bonus
        modifier += (proficiency_bonus * 2)
        self.assertEqual(character_skill.modifier, modifier)


class ClassTestCase(TestCase):
    fixtures = (
        '0001_sources.json',
        '0007_classes'
    )

    def test__str__returns_correct_value(self):
        class_instance = Class.objects.first()
        self.assertEqual(str(class_instance), class_instance.name)


class LevelTestCase(TestCase):
    fixtures = (
        '0001_levels.json',
    )

    def test__str__returns_correct_value(self):
        level = Level.objects.first()
        self.assertEqual(int(str(level)), level.value)
