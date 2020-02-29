from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer
from core.utils import get_ability_name


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    @action(detail=True, methods=['get'])
    def abilities(self, request, pk=None):
        character = self.get_object()
        data = []
        for character_ability in character.character_abilities.all():
            ability_name = get_ability_name(character_ability.ability)
            data.append({
                'ability': ability_name,
                'modifier': character_ability.modifier,
                'value': character_ability.value
            })
        return Response(data, status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def skills(self, request, pk=None):
        character = self.get_object()
        data = []
        for character_skill in character.character_skills.select_related('skill').all():
            data.append({
                'modifier': character_skill.modifier,
                'proficiency': character_skill.proficiency,
                'skill': character_skill.skill.name
            })
        return Response(data, status.HTTP_200_OK)

