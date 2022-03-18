import rest_framework.permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import (BasePermission, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from map.api import serializers
from map.models import Point
from map.utils.telegram import send_message_about_verification


class IsPointOwnerOrSuperuser(BasePermission):  # TODO move to permissions dir
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in rest_framework.permissions.SAFE_METHODS or
            (
                obj.created_by == request.user or
                request.user.is_superuser
            )
        )


class PointViewSet(viewsets.ModelViewSet):
    """TODO"""

    queryset = Point.objects.all()
    serializer_class = serializers.PointCreateUpdateSerializerUser
    permission_classes = (IsAuthenticatedOrReadOnly, IsPointOwnerOrSuperuser)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return serializers.PointListRetrieveSerializer
        if self.action == "create" and self.request.user.is_superuser:
            return serializers.PointCreateUpdateSerializerAdmin
        if self.action == "retrieve" and self.request.user.is_superuser:
            return serializers.PointCreateUpdateSerializerAdmin
        if (self.action == "update" or self.action == "partial_update") and self.request.user.is_superuser:
            return serializers.PointCreateUpdateSerializerAdmin
        return super().get_serializer_class()

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_verified'):
            send_message_about_verification('create', self.get_object())
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        before_update = self.get_object().is_verified
        after_update = serializer.validated_data['is_verified']
        if before_update is False and after_update is True:
            send_message_about_verification('update', self.get_object())
        serializer.save()
