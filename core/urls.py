from rest_framework import routers

from core.views import DiceViewSet, FeatureViewSet, SkillViewSet

router = routers.SimpleRouter()
router.register(r'dice', DiceViewSet)
router.register(r'feature', FeatureViewSet)
router.register(r'skill', SkillViewSet)
urlpatterns = router.urls
