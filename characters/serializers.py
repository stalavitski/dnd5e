from rest_framework import serializers

from characters.models import Character, CharacterAbility, CharacterSavingThrow, CharacterSkill


class CharacterAbilitySerializer(serializers.ModelSerializer):
    ability = serializers.CharField(read_only=True, source='ability_name')
    modifier = serializers.IntegerField(read_only=True)

    class Meta:
        exclude = ('character', 'created_at', 'deleted_at', 'updated_at')
        model = CharacterAbility

class CharacterSavingThrowSerializer(serializers.ModelSerializer):
    ability = serializers.CharField(read_only=True, source='ability_name')
    modifier = serializers.IntegerField(read_only=True)

    class Meta:
        exclude = ('character', 'created_at', 'deleted_at', 'updated_at')
        model = CharacterSavingThrow


class CharacterSerializer(serializers.ModelSerializer):
    armor_class = serializers.IntegerField(read_only=True)
    background_name = serializers.CharField(read_only=True, source='background.name')
    initiative = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True, source='level.value')
    proficiency_bonus = serializers.IntegerField(read_only=True, source='level.proficiency_bonus')
    speed = serializers.IntegerField(read_only=True)

    class Meta:
        exclude = ('created_at', 'deleted_at', 'skills', 'updated_at')
        model = Character


class CharacterSkillSerializer(serializers.ModelSerializer):
    modifier = serializers.IntegerField(read_only=True)
    skill = serializers.CharField(read_only=True, source='skill.name')

    class Meta:
        exclude = ('character', 'created_at', 'deleted_at', 'updated_at')
        model = CharacterSkill
