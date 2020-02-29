from rest_framework import serializers

from characters.models import Character

from core.data import ABILITY_DICT


class CharacterAbilitiesField(serializers.Field):
    def get_attribute(self, instance):
        return instance.character_abilities.all()

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        representation = []
        for character_ability in value:
            ability_name = ABILITY_DICT[character_ability.ability]
            representation.append({
                "ability": ability_name,
                "modifier": character_ability.modifier,
                "value": character_ability.value
            })
        return representation


class CharacterSkillsField(serializers.Field):
    def get_attribute(self, instance):
        return instance.character_skills.select_related('skill').all()

    def to_internal_value(self, data):
        pass

    def to_representation(self, value):
        representation = []
        for character_skill in value:
            representation.append({
                "modifier": character_skill.modifier,
                "proficiency": character_skill.proficiency,
                "skill": character_skill.skill.name
            })
        return representation


class CharacterSerializer(serializers.ModelSerializer):
    abilities = CharacterAbilitiesField()
    initiative = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True, source='level.value')
    proficiency_bonus = serializers.IntegerField(read_only=True, source='level.proficiency_bonus')
    skills = CharacterSkillsField()

    class Meta:
        exclude = ()
        model = Character
