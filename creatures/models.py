from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_paranoid.models import ParanoidModel

from core.data import ABILITY_CHOICES
from creatures.data import PROFICIENCY_CHOICES, PROFICIENCY_PROF
from creatures.utils import get_proficiency_verbose


class Language(ParanoidModel):
    is_exotic = models.BooleanField(default=False)
    name = models.CharField(max_length=20, unique=True)
    script = models.ForeignKey('creatures.Script', models.CASCADE, 'languages', blank=True, null=True)

    def __str__(self):
        return self.name


class Race(ParanoidModel):
    age = models.TextField(blank=True)
    alignment = models.TextField(blank=True)
    climb_speed = models.IntegerField(
        blank=True, default=None, null=True, validators=[MinValueValidator(10), MaxValueValidator(100)])
    climb_speed_description = models.TextField(blank=True)
    flight_speed = models.IntegerField(
        blank=True, default=None, null=True, validators=[MinValueValidator(10), MaxValueValidator(100)])
    flight_speed_description = models.TextField(blank=True)
    languages = models.ManyToManyField('creatures.Language', 'races', through='creatures.RacialLanguage')
    name = models.CharField(max_length=50, unique=True)
    source = models.ForeignKey('core.Source', models.CASCADE, 'races')
    size = models.ForeignKey('creatures.Size', models.CASCADE, 'races')
    size_description = models.TextField(blank=True)
    skills = models.ManyToManyField('core.Skill', 'races', through='creatures.RacialSkill')
    speed = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])
    speed_description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class RacialAbility(ParanoidModel):
    MIN_VALUE = -2
    MAX_VALUE = +2

    ability = models.CharField(choices=ABILITY_CHOICES, max_length=3)
    race = models.ForeignKey('creatures.Race', models.CASCADE, 'racial_abilities')
    value = models.IntegerField(validators=[MinValueValidator(MIN_VALUE), MaxValueValidator(MAX_VALUE)])

    def __str__(self):
        return 'Race: {}, Ability Score Increase: {} {}'.format(self.race.name, self.ability, self.value)


class RacialLanguage(ParanoidModel):
    language = models.ForeignKey('creatures.Language', models.CASCADE, 'racial_languages')
    race = models.ForeignKey('creatures.Race', models.CASCADE, 'racial_languages')

    def __str__(self):
        return 'Race: {}, Language: {}'.format(self.race.name, self.language.name)


class RacialSkill(ParanoidModel):
    race = models.ForeignKey('creatures.Race', models.CASCADE, 'racial_skills')
    proficiency = models.CharField(choices=PROFICIENCY_CHOICES, default=PROFICIENCY_PROF, max_length=11)
    skill = models.ForeignKey('core.Skill', models.CASCADE, 'racial_skills')

    def __str__(self):
        verbal_proficiency = get_proficiency_verbose(self.proficiency)
        return 'Race: {}, Skill Proficiency: {} {}'.format(self.race.name, self.skill.name, verbal_proficiency)


class Script(ParanoidModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Sense(ParanoidModel):
    description = models.TextField(blank=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Size(ParanoidModel):
    name = models.TextField(unique=True)
    space = models.CharField(max_length=50)
    value = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


# @TODO Add RacialFeatures, RacialSenses and RacialResistances
