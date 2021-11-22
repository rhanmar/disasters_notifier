from rest_framework import serializers
from map.models import Point


class PointSerializer(serializers.ModelSerializer):
    """TODO"""

    # created_at  TODO
    # modified_at TODO

    class Meta:
        model = Point
        fields = '__all__'  # TODO
