from rest_framework import routers

from characters.routers import CharacterDetailsRouter
from characters.views import (
    CharacterAbilityViewSet,
    CharacterDetailsViewSet,
    CharacterSavingThrowViewSet,
    CharacterSkillViewSet,
    CharacterViewSet
)

character_details_router = CharacterDetailsRouter()
character_details_router.register(r'(?P<character_id>[0-9]+)/details', CharacterDetailsViewSet, 'character-details')

router = routers.DefaultRouter()
router.register(r'(?P<character_id>[0-9]+)/ability', CharacterAbilityViewSet, 'character-ability')
# router.register(r'details', CharacterDetailsViewSet, 'character-details')
router.register(
    r'(?P<character_id>[0-9]+)/saving-throw',
    CharacterSavingThrowViewSet,
    'character-saving-throw'
)
router.register(r'(?P<character_id>[0-9]+)/skill', CharacterSkillViewSet, 'character-skill')
router.register(r'', CharacterViewSet)

urlpatterns = character_details_router.urls + router.urls
