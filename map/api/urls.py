from rest_framework import routers

from map.api.views import PointViewSet

router = routers.DefaultRouter()
router.register("points", PointViewSet, basename="point")

urlpatterns = router.urls
