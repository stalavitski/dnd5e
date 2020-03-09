import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_paranoid.models import ParanoidModel

from core.data import ABILITY_CHOICES


class Dice(ParanoidModel):
    sides = models.IntegerField(unique=True, validators=[MinValueValidator(2), MaxValueValidator(100)])

    def __str__(self):
        return 'd{}'.format(self.sides)

    def roll(self):
        return random.randint(1, self.sides)


class Feature(ParanoidModel):
    name = models.CharField(max_length=15, unique=True)
    source = models.ForeignKey('core.Source', models.CASCADE, 'features')

    def __str__(self):
        return self.name


class Skill(ParanoidModel):
    ability = models.CharField(choices=ABILITY_CHOICES, max_length=3)
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Source(ParanoidModel):
    name = models.CharField(max_length=40, unique=True)
    short_name = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return self.name
