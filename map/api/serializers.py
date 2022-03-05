from rest_framework import serializers
from map.models import Point


class PointListRetrieveSerializer(serializers.ModelSerializer):
    """TODO"""

    # created_at  TODO
    # modified_at TODO
    created_by = serializers.IntegerField(source="created_by_id")
    translated_disaster_type = serializers.CharField(source="get_translated_disaster_type")
    # is_verified = serializers.CharField(source="get_translated_is_verified")

    class Meta:
        model = Point
        fields = '__all__'  # TODO.

    # def create(self, validated_data):
    #     validated_data["created_by"] = self.context["request"].user
    #     print("!!!!")
    #     return super().create(validated_data)

#      https://github.com/rhanmar/oi_projects_summer_2021/blob/main/camp-python-2021-find-me-develop/apps/map/api/serializers.py#L112
# https://stackoverflow.com/questions/30203652/how-to-get-request-user-in-django-rest-framework-serializer
# https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context


# class PointCreateSerializerAdmin(serializers.ModelSerializer):
class PointCreateUpdateSerializerAdmin(serializers.ModelSerializer):
    # created_by = serializers.IntegerField(source="created_by_id")

    class Meta:
        model = Point
        fields = [
            "id",
            "name",
            "description",
            "coordinates",
            "created_at",
            "updated_at",
            "disaster_type",
            "disaster_level",
            "is_verified",
        ]


class PointCreateUpdateSerializerUser(serializers.ModelSerializer):
    # created_by = serializers.IntegerField(source="created_by_id")

    class Meta:
        model = Point
        fields = [
            "id",
            "name",
            "description",
            "coordinates",
            "created_at",
            "updated_at",
            "disaster_type",
            "disaster_level",
        ]
