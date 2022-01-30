from django.test import TestCase
from rest_framework.authtoken.models import Token

from users.factories import UserFactory


class UserTest(TestCase):

    def test_token_creation_after_signing_up(self):
        user = UserFactory()
        self.assertTrue(Token.objects.filter(user=user).exists())
