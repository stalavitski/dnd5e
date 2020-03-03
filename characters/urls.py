from rest_framework import routers

from characters.views import (
    CharacterAbilityViewSet,
    CharacterSavingThrowViewSet,
    CharacterSkillViewSet,
    CharacterViewSet
)

router = routers.DefaultRouter()
router.register(r'character-ability/(?P<character_id>[0-9]+)', CharacterAbilityViewSet, 'character-ability')
router.register(
    r'character-saving-throw/(?P<character_id>[0-9]+)',
    CharacterSavingThrowViewSet,
    'character-saving-throw'
)
router.register(r'character-skill/(?P<character_id>[0-9]+)', CharacterSkillViewSet, 'character-skill')
router.register(r'character', CharacterViewSet)

urlpatterns = router.urls
