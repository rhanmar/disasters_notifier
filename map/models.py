from django.db import models
# from django.contrib.gis.db import models TODO


class Point(models.Model):
    """Model for map Point"""

    DISASTER_LEVELS = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    DISASTER_TYPES = [("fire", "fire"), ("water", "water"), ("geo", "geo"), ("meteo", "meteo")]

    name = models.CharField(max_length=120)
    coordinates = models.CharField(max_length=80)
    # coordinates = models.PointField() TODO
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    disaster_type = models.CharField(
        max_length=80,
        choices=DISASTER_TYPES
        ,
        default="fire",
    )
    disaster_level = models.CharField(
        max_length=1,
        choices=DISASTER_LEVELS,
        default=1,
    )
    # owner TODO
