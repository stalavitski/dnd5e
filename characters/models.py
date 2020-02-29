import math

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django_paranoid.models import ParanoidModel

from core.data import ABILITY_CHOICES, ABILITY_DEXTERITY

class Background(ParanoidModel):
    name = models.CharField(max_length=30, unique=True)
    source = models.ForeignKey('core.Source', models.CASCADE, 'backgrounds')

    def __str__(self):
        return self.name


class Character(ParanoidModel):
    background = models.ForeignKey('characters.Background', models.CASCADE, 'characters')
    experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(355000)])
    name = models.CharField(max_length=50)
    skills = models.ManyToManyField('core.Skill', 'characters', through='characters.CharacterSkill')

    def __str__(self):
        return self.name

    @cached_property
    def level(self):
        return (
            Level
                .objects
                .order_by('required_experience')
                .filter(required_experience__lte=self.experience)
                .last()
        )

    @cached_property
    def initiative(self):
        return self.character_abilities.get(ability=ABILITY_DEXTERITY).modifier


class CharacterAbility(ParanoidModel):
    AVERAGE_VALUE = 10
    MAX_VALUE = 20
    MIN_VALUE = 8

    ability = models.CharField(choices=ABILITY_CHOICES, max_length=3)
    character = models.ForeignKey('characters.Character', models.CASCADE, 'character_abilities')
    value = models.IntegerField(
        default=MIN_VALUE,
        validators=[MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE)]
    )

    class Meta:
        unique_together = [['ability', 'character']]

    @property
    def modifier(self):
        return math.floor((self.value - self.AVERAGE_VALUE) / 2)


class CharacterSkill(ParanoidModel):
    PROFICIENCY_NONE = 'none'
    PROFICIENCY_PROF = 'proficiency'
    PROFICIENCY_EXP = 'expertise'

    PROFICIENCY_CHOICES = (
        (PROFICIENCY_NONE, 'None'),
        (PROFICIENCY_PROF, 'Proficiency'),
        (PROFICIENCY_EXP, 'Expertise')
    )

    character = models.ForeignKey('characters.Character', models.CASCADE, 'character_skills')
    proficiency = models.CharField(choices=PROFICIENCY_CHOICES, default=PROFICIENCY_NONE, max_length=11)
    skill = models.ForeignKey('core.Skill', models.CASCADE, 'character_skills')

    class Meta:
        unique_together = [['character', 'skill']]

    @cached_property
    def modifier(self):
        character_ability = CharacterAbility.objects.get(character=self.character, ability=self.skill.ability)
        # Calculate modifier depends on proficiency
        if self.proficiency == self.PROFICIENCY_NONE:
            return character_ability.modifier
        else:
            proficiency_modifier = self.character.level.proficiency_bonus
            # Proficiency modifier is doubled for skill with expertise
            if self.proficiency is self.PROFICIENCY_EXP:
                proficiency_modifier *= 2
            return character_ability.modifier + proficiency_modifier


class Class(ParanoidModel):
    name = models.CharField(max_length=15, unique=True)
    source = models.ForeignKey('core.Source', models.CASCADE, 'classes')

    def __str__(self):
        return self.name


class Level(ParanoidModel):
    proficiency_bonus = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(6)])
    required_experience = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(355000)])
    value = models.IntegerField(unique=True, validators=[MinValueValidator(1), MaxValueValidator(20)])

    def __str__(self):
        return str(self.value)
