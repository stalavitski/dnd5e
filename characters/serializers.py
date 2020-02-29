from rest_framework import serializers

from characters.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    initiative = serializers.IntegerField(read_only=True)
    level = serializers.IntegerField(read_only=True, source='level.value')
    proficiency_bonus = serializers.IntegerField(read_only=True, source='level.proficiency_bonus')

    class Meta:
        exclude = ('created_at', 'deleted_at', 'skills', 'updated_at')
        model = Character
