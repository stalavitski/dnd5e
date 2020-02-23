import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Ability(models.Model):
    name = models.CharField(max_length=15)


class Dice(models.Model):
    sides = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(100)])

    def __str__(self):
        return 'd{}'.format(self.sides)

    def roll(self):
        return random.randint(1, self.sides)


class Feature(models.Model):
    name = models.CharField(max_length=15)


class Skill(models.Model):
    ability = models.ForeignKey('core.Ability', models.CASCADE, related_name='skills')
    name = models.CharField(max_length=15)
