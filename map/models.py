from django.db import models
# from django.contrib.gis.db import models TODO
# from django.contrib.auth.models import User
from users.models import User


class Point(models.Model):
    """Model for map Point"""

    DISASTER_LEVELS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    DISASTER_TYPES = [("fire", "fire"), ("water", "water"), ("geo", "geo"), ("meteo", "meteo")]

    name = models.CharField(max_length=120)
    coordinates = models.CharField(max_length=80)
    # coordinates = models.PointField() TODO
    created_at = models.DateTimeField(auto_now_add=True)  # TODO create TimeStampMixin
    modified_at = models.DateTimeField(auto_now=True)  # TODO create TimeStampMixin
    verified = models.BooleanField(default=False)
    disaster_type = models.CharField(
        max_length=80,
        choices=DISASTER_TYPES,
        default="fire",
    )
    disaster_level = models.CharField(
        max_length=1,
        choices=DISASTER_LEVELS,
        default=1,
    )
    created_by = models.ForeignKey(
        User,
        related_name="created_points",
        on_delete=models.CASCADE,
    )
