from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime


@receiver(pre_save, sender='users.User')
def set_unique_code(sender, instance, *args, **kwargs):
    now = str(datetime.now())
    instance.unique_code = hash(f"{instance.id}{instance.first_name}{instance.last_name}{now}")
