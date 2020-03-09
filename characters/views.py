from djangorestframework_camel_case import parser
from rest_framework import decorators, mixins, viewsets

from characters.models import Character, CharacterAbility, CharacterDetails, CharacterSavingThrow, CharacterSkill
from characters.serializers import (
    CharacterAbilitySerializer,
    CharacterDetailsPortraitSerializer,
    CharacterDetailsSerializer,
    CharacterSavingThrowSerializer,
    CharacterSerializer,
    CharacterSkillSerializer
)


class CharacterAbilityViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    serializer_class = CharacterAbilitySerializer

    def get_queryset(self): # pragma: no cover
        character_id = self.kwargs.get('character_id')
        return CharacterAbility.objects.filter(character_id=character_id)


class CharacterDetailsViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    lookup_field = 'character_id'
    serializer_class = CharacterDetailsSerializer
    queryset = CharacterDetails.objects.select_related('player').all()

    @decorators.action(
        detail=True,
        methods=['patch'],
        parser_classes=[parser.CamelCaseMultiPartParser],
        serializer_class=CharacterDetailsPortraitSerializer
    )
    def portrait(self, request, character_id): # pragma: no cover
        return self.update(request, character_id)


class CharacterSavingThrowViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    serializer_class = CharacterSavingThrowSerializer

    def get_queryset(self): # pragma: no cover
        character_id = self.kwargs.get('character_id')
        return CharacterSavingThrow.objects.select_related('character').filter(character_id=character_id)


class CharacterSkillViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    http_method_names = ['get', 'head', 'patch']
    serializer_class = CharacterSkillSerializer

    def get_queryset(self): # pragma: no cover
        character_id = self.kwargs.get('character_id')
        return CharacterSkill.objects.select_related('character', 'skill').filter(character_id=character_id)


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
