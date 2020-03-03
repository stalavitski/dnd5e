from rest_framework import routers

from characters.views import (
    CharacterAbilityViewSet,
    CharacterSavingThrowViewSet,
    CharacterSkillViewSet,
    CharacterViewSet
)

router = routers.DefaultRouter()
router.register(r'(?P<character_id>[0-9]+)/ability', CharacterAbilityViewSet, 'character-ability')
router.register(
    r'(?P<character_id>[0-9]+)/saving-throw',
    CharacterSavingThrowViewSet,
    'character-saving-throw'
)
router.register(r'(?P<character_id>[0-9]+)/skill', CharacterSkillViewSet, 'character-skill')
router.register(r'', CharacterViewSet)

urlpatterns = router.urls
