from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender='users.User')
def generate_token_for_new_user(sender, instance, created=False, *args, **kwargs) -> None:
    """Generate DRF Token for new User."""
    if created:
        Token.objects.create(user=instance)
