from rest_framework import routers

from characters.views import CharacterViewSet

router = routers.DefaultRouter()
router.register(r'api/character', CharacterViewSet)
urlpatterns = router.urls
