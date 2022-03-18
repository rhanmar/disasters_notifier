import factory

from map.models import Point
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating new User."""
    class Meta:
        model = User

    username = factory.Faker('first_name')


class PointFactory(factory.django.DjangoModelFactory):
    """Factory for creating new Point."""
    class Meta:
        model = Point

    name = factory.Faker('text')
    coordinates = f"{factory.Faker('latitude')}, {factory.Faker('longitude')}"
    created_by = factory.SubFactory(UserFactory)
