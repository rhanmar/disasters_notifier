from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from users.signals import generate_token_for_new_user
from django.template.defaultfilters import slugify


class User(AbstractUser):
    """Model for User."""

    telegram_id = models.CharField(
        max_length=128,
        blank=True,
    )

    @property
    def has_telegram_account(self) -> bool:
        if self.telegram_id:
            return True
        return False

    @property
    def get_slug(self) -> str:
        data = list()
        data.append(str(self.pk))
        if self.username:
            data.append(self.username)
        if self.first_name:
            data.append(self.first_name)
        if self.last_name:
            data.append(self.last_name)
        return slugify(' '.join(data))


post_save.connect(generate_token_for_new_user, User)
