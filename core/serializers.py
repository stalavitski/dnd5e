from rest_framework import serializers

from core.models import Ability, Dice, Feature, Skill


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ()
        model = Ability


class DiceSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ()
        model = Dice


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ()
        model = Feature


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ()
        model = Skill
