from rest_framework import serializers

from characters.models import Character, CharacterAbility, CharacterDetails, CharacterSavingThrow, CharacterSkill


class CharacterAbilitySerializer(serializers.ModelSerializer):
    ability = serializers.CharField(read_only=True, source='ability_name')
    initial_value = serializers.IntegerField(write_only=True)
    modifier = serializers.IntegerField(read_only=True)
    value = serializers.IntegerField(read_only=True)

    class Meta:
        exclude = ('character', 'created_at', 'deleted_at', 'updated_at')
        model = CharacterAbility


class CharacterDetailsSerializer(serializers.ModelSerializer):
    player = serializers.CharField(read_only=True, source='player.first_name')
    portrait = serializers.ImageField(read_only=True)

    class Meta:
        exclude = ('character', 'created_at', 'deleted_at', 'updated_at')
        model = CharacterDetails


class CharacterDetailsPortraitSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('portrait',)
        model = CharacterDetails


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
    race_name = serializers.CharField(read_only=True, source='race.name')
    speed = serializers.IntegerField(read_only=True)

    class Meta:
        exclude = ('created_at', 'deleted_at', 'skills', 'updated_at')
        model = Character


class CharacterSkillSerializer(serializers.ModelSerializer):
    modifier = serializers.IntegerField(read_only=True)
    initial_proficiency = serializers.IntegerField(write_only=True)
    proficiency = serializers.CharField(read_only=True)
    skill = serializers.CharField(read_only=True, source='skill.name')

    class Meta:
        exclude = ('character', 'created_at', 'deleted_at', 'updated_at')
        model = CharacterSkill
