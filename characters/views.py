from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from characters.models import Character, CharacterAbility, CharacterSavingThrow, CharacterSkill
from characters.serializers import (
    CharacterAbilitySerializer,
    CharacterSerializer,
    CharacterSavingThrowSerializer,
    CharacterSkillSerializer
)
from core.utils import get_ability_name


class CharacterAbilityViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    serializer_class = CharacterAbilitySerializer

    def get_queryset(self):
        character_id = self.kwargs.get('character_id')
        return CharacterAbility.objects.filter(character_id=character_id)


class CharacterSavingThrowViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    serializer_class = CharacterSavingThrowSerializer

    def get_queryset(self):
        character_id = self.kwargs.get('character_id')
        return CharacterSavingThrow.objects.select_related('character').filter(character_id=character_id)


class CharacterSkillViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    serializer_class = CharacterSkillSerializer

    def get_queryset(self):
        character_id = self.kwargs.get('character_id')
        return CharacterSkill.objects.select_related('character', 'skill').filter(character_id=character_id)


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
