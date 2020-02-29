from rest_framework import viewsets

from core.models import Dice, Feature, Skill
from core.serializers import DiceSerializer, FeatureSerializer, SkillSerializer


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
