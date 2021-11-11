from rest_framework import viewsets
from map.models import Point
from map.api.serializers import PointSerializer


class PointViewSet(viewsets.ModelViewSet):
    """TODO"""

    queryset = Point.objects.all()
    serializer_class = PointSerializer
