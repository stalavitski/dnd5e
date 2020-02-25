import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_paranoid.models import ParanoidModel


class Ability(ParanoidModel):
    name = models.CharField(max_length=15)


class Dice(ParanoidModel):
    sides = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(100)])

    def __str__(self):
        return 'd{}'.format(self.sides)

    def roll(self):
        return random.randint(1, self.sides)


class Feature(ParanoidModel):
    name = models.CharField(max_length=15)


class Skill(ParanoidModel):
    ability = models.ForeignKey('core.Ability', models.CASCADE, related_name='skills')
    name = models.CharField(max_length=15)
