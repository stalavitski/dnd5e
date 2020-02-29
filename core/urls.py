from rest_framework import routers

from core.views import DiceViewSet, FeatureViewSet, SkillViewSet

router = routers.DefaultRouter()
router.register(r'api/dice', DiceViewSet)
router.register(r'api/feature', FeatureViewSet)
router.register(r'api/skill', SkillViewSet)
urlpatterns = router.urls
