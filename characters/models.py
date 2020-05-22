import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils.functional import cached_property
from django_paranoid.models import ParanoidModel
from django_resized import ResizedImageField

from characters.data import (
    ALIGNMENT_CHOICES,
    GENDER_CHOICES,
    MAX_EXP,
    PROFICIENCY_CHOICES,
    PROFICIENCY_EXP,
    PROFICIENCY_NONE
)
from characters.utils import get_proficiency_by_priority, portrait_upload_to
from core.data import ABILITY_CHOICES, ABILITY_DEXTERITY, ABILITY_DICT
from core.models import Skill
from core.utils import get_ability_name


class Background(ParanoidModel):
    name = models.CharField(max_length=30, unique=True)
    source = models.ForeignKey('core.Source', models.CASCADE, 'backgrounds')

    def __str__(self):
        return self.name


class Character(ParanoidModel):
    BASE_ARMOR = 10

    background = models.ForeignKey('characters.Background', models.CASCADE, 'characters', blank=True, null=True)
    experience = models.IntegerField(default=0, validators=(MinValueValidator(0), MaxValueValidator(MAX_EXP)))
    name = models.CharField(blank=True, max_length=50)
    race = models.ForeignKey('creatures.Race', models.CASCADE, 'characters')
    skills = models.ManyToManyField('core.Skill', 'characters', through='characters.CharacterSkill')

    def __str__(self):
        return self.name

    @cached_property
    def armor_class(self):
        return self.BASE_ARMOR + self.dex_modifier

    @cached_property
    def dex_modifier(self):
        return self.character_abilities.get(ability=ABILITY_DEXTERITY).modifier

    @cached_property
    def initiative(self):
        return self.dex_modifier

    @cached_property
    def level(self):
        return (
            Level.objects
                .order_by('required_experience')
                .filter(required_experience__lte=self.experience)
                .last()
        )

    @transaction.atomic
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        adding = self._state.adding
        super().save(force_insert, force_update, using, update_fields)
        # Create default relations when record is created
        if adding:
            # Create default abilities and saving throws
            for ability in ABILITY_DICT.keys():
                self.character_abilities.create(ability=ability)
                self.character_saving_throws.create(ability=ability)
            # Create default skills
            skill_ids = Skill.objects.values_list('id', flat=True)
            for skill_id in skill_ids:
                self.character_skills.create(skill_id=skill_id)
            # Create a character details relation
            CharacterDetails.objects.create(character=self, player_id=1)

    @cached_property
    def speed(self):
        return self.race.speed


class CharacterAbility(ParanoidModel):
    AVERAGE_VALUE = 10
    MAX_VALUE = 20
    MIN_VALUE = 8

    ability = models.CharField(choices=ABILITY_CHOICES, max_length=3)
    initial_value = models.IntegerField(
        default=MIN_VALUE,
        validators=(MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE))
    )
    character = models.ForeignKey('characters.Character', models.CASCADE, 'character_abilities')

    class Meta:
        unique_together = (('ability', 'character'),)

    def __str__(self):
        return '{} Ability'.format(self.ability_name)

    @property
    def ability_name(self):
        return get_ability_name(self.ability)

    @property
    def modifier(self):
        return math.floor((self.value - self.AVERAGE_VALUE) / 2)

    @cached_property
    def value(self):
        value = self.initial_value
        racial_ability_increase = (
            self.character.race.racial_abilities
                .filter(ability=self.ability)
                .values_list('value', flat=True)
                .first()
        ) or 0
        value += racial_ability_increase
        return value


class CharacterDetails(ParanoidModel):
    age = models.IntegerField(blank=True, null=True)
    alignment = models.CharField(blank=True, choices=ALIGNMENT_CHOICES, max_length=2)
    appearance = models.TextField(blank=True)
    portrait = ResizedImageField(crop=('top', 'right'), null=True, size=(300, 300), upload_to=portrait_upload_to)
    character = models.OneToOneField('characters.Character', models.CASCADE, related_name='details')
    eyes = models.CharField(blank=True, max_length=60)
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=1)
    hair = models.CharField(blank=True, max_length=60)
    height = models.IntegerField(blank=True, help_text='In inches', null=True)
    history = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    organizations = models.TextField(blank=True, help_text='Allies and Organizations')
    player = models.ForeignKey('users.User', models.CASCADE)
    skin = models.CharField(blank=True, max_length=60)
    weight = models.IntegerField(blank=True, help_text='In pounds', null=True)


class CharacterSavingThrow(ParanoidModel):
    ability = models.CharField(choices=ABILITY_CHOICES, max_length=3)
    character = models.ForeignKey('characters.Character', models.CASCADE, 'character_saving_throws')
    is_proficient = models.BooleanField(default=False)

    class Meta:
        unique_together = (('ability', 'character'),)

    def __str__(self):
        return '{} Saving Throw'.format(self.ability_name)

    @property
    def ability_name(self):
        return get_ability_name(self.ability)

    @property
    def modifier(self):
        character_ability = self.character.character_abilities.get(ability=self.ability)
        modifier = character_ability.modifier
        # Add proficiency bonus if proficient
        if self.is_proficient:
            modifier += self.character.level.proficiency_bonus
        return modifier

class CharacterSkill(ParanoidModel):
    character = models.ForeignKey('characters.Character', models.CASCADE, 'character_skills')
    initial_proficiency = models.CharField(choices=PROFICIENCY_CHOICES, default=PROFICIENCY_NONE, max_length=11)
    skill = models.ForeignKey('core.Skill', models.CASCADE, 'character_skills')

    class Meta:
        unique_together = (('character', 'skill'),)

    def __str__(self):
        return 'Character: {}, Skill: {}'.format(self.character.name, self.skill.name)

    @cached_property
    def modifier(self):
        character_ability = self.character.character_abilities.get(ability=self.skill.ability)
        # Calculate modifier depends on proficiency
        if self.proficiency == PROFICIENCY_NONE:
            return character_ability.modifier
        else:
            proficiency_modifier = self.character.level.proficiency_bonus
            # Proficiency modifier is doubled for skill with expertise
            if self.proficiency is PROFICIENCY_EXP:
                proficiency_modifier *= 2
            return character_ability.modifier + proficiency_modifier


    @cached_property
    def proficiency(self):
        racial_proficiency = (
            self.character.race.racial_skills
                .filter(skill=self.skill)
                .values_list('proficiency', flat=True)
                .first()
        )
        return get_proficiency_by_priority(self.initial_proficiency, racial_proficiency)


class Class(ParanoidModel):
    name = models.CharField(max_length=15, unique=True)
    source = models.ForeignKey('core.Source', models.CASCADE, 'classes')

    def __str__(self):
        return self.name


class Level(ParanoidModel):
    proficiency_bonus = models.IntegerField(validators=(MinValueValidator(2), MaxValueValidator(6)))
    required_experience = models.IntegerField(validators=(MinValueValidator(0), MaxValueValidator(MAX_EXP)))
    value = models.IntegerField(unique=True, validators=(MinValueValidator(1), MaxValueValidator(20)))

    def __str__(self):
        return str(self.value)
