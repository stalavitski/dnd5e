from rest_framework import viewsets

from core.models import Ability, Dice, Feature, Skill
from core.serializers import AbilitySerializer, DiceSerializer, FeatureSerializer, SkillSerializer


class AbilityViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'put']
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


class DiceViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'put']
    queryset = Dice.objects.all()
    serializer_class = DiceSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer


class SkillViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'head', 'patch', 'put']
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
