import rest_framework.permissions
from rest_framework import viewsets
from map.models import Point
from map.api import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from map.utils.telegram import send_message_about_verification_to_channel


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
    # serializer_class = PointSerializer
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

    # def create(self, request, *args, **kwargs):
    #     print("???? CREATE")
    #     import ipdb; ipdb.set_trace()
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)
    #     print(serializer.is_valid())
    #     print(serializer.errors)
    #     print(serializer.data)

    # v2
    # def create(self, request, *args, **kwargs):
    #     import ipdb;
    #     ipdb.set_trace()
    #     data = request.data.dict()
    #     data["created_by"] = request.user.id
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if serializer.validated_data.get('is_verified'):
            send_message_about_verification_to_channel('create')
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        before_update = self.get_object().is_verified
        after_update = serializer.validated_data['is_verified']
        if before_update is False and after_update is True:
            send_message_about_verification_to_channel('update')
        serializer.save()
