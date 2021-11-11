from django.urls import include, path
from rest_framework import routers
from map.api.views import PointViewSet

router = routers.DefaultRouter()
router.register('points', PointViewSet)

urlpatterns = router.urls
