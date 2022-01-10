from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from users.signals import set_unique_code


class User(AbstractUser):

    telegram_id = models.CharField(
        max_length=128,
        blank=True,
    )
    unique_code = models.CharField(
        max_length=128,
    )


pre_save.connect(set_unique_code, User)
