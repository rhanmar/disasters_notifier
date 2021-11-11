from django.db import models
# from django.contrib.gis.db import models TODO


class Point(models.Model):
    """Model for map Point"""

    name = models.CharField(max_length=120)
    coordinates = models.CharField(max_length=80)
    # coordinates = models.PointField() TODO
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    # owner TODO
