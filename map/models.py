from django.db import models
from users.models import User
from django.utils.translation import gettext as _


class DisasterTypes:
     FIRE = "FIRE"
     WATER = "WATER"
     GEO = "GEO"
     METEO = "METEO"
     UNKNOWN = "UNKNOWN"

     RESOLVER = {
        FIRE: _("Пожар"),
        WATER: _("Гидрологический характер"),
        GEO: _("Геологический характер"),
        METEO: _("Метеорологический характер"),
     }
     CHOICES = RESOLVER.items()


class TimestampedMixin(models.Model):
    """TODO"""
    created_at = models.DateTimeField(
        verbose_name=_('Дата создания'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Дата изменения'),
        auto_now=True,
    )

    class Meta:
        abstract = True


class Point(TimestampedMixin, models.Model):
    """Model for map Point"""

    DISASTER_LEVELS = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    # DISASTER_TYPES = [("fire", "fire"), ("water", "water"), ("geo", "geo"), ("meteo", "meteo")]

    name = models.CharField(
        verbose_name=_('Наименование точки'),
        max_length=120
    )
    description = models.CharField(
        verbose_name=_('Описание точки'),
        max_length = 360,
        blank=True
    )
    coordinates = models.CharField(
        verbose_name=_("Коордиаты точки"),
        max_length=80
    )
    # created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(
       verbose_name=_("Подтверждена ли точка"),
        default=False,
        help_text=_(
            "Подтверждена ли точка уполномоченным лицом или организацией. Значение по умолчанию: не подтверждено"
        )
    )
    disaster_type = models.CharField(
        verbose_name=_("Тип стихийного бедствия"),
        max_length=80,
        choices=DisasterTypes.CHOICES,
        default=DisasterTypes.UNKNOWN,
    )
    disaster_level = models.SmallIntegerField(
        verbose_name=_("Уровень опасности стихийного бедствия"),
        choices=DISASTER_LEVELS,
        default=0,
    )
    created_by = models.ForeignKey(
        verbose_name=_("Автор точки"),
        to=User,
        related_name="created_points",
        on_delete=models.CASCADE,
    )

    @property
    def get_translated_disaster_type(self):
        return DisasterTypes.RESOLVER[self.disaster_type]

    @property
    def get_translated_is_verified(self):
        if self.is_verified:
            return "Подтверждено"
        return  "Не подтверждено"

    def __str__(self):
        return f"{self.name} - {self.disaster_type} - {self.disaster_level} - {self.is_verified}"
