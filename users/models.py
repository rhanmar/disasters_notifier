from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from users.signals import generate_token_for_new_user


class User(AbstractUser):

    telegram_id = models.CharField(
        max_length=128,
        blank=True,
    )


post_save.connect(generate_token_for_new_user, User)
