import ipdb
from rest_framework import viewsets
from map.models import Point
from map.api.serializers import PointSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission


# class IsSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_superuser

    # def has_object_permission(self, request, view, obj):
    #     return obj

# class IsPointOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user

class IsPointOwnerOrSuperuser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.user.is_superuser


class PointViewSet(viewsets.ModelViewSet):
    """TODO"""

    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def create(self, request, *args, **kwargs):
    #     print("???? CREATE")
    #     import ipdb; ipdb.set_trace()
    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)
    #     print(serializer.is_valid())
    #     print(serializer.errors)
    #     print(serializer.data)
