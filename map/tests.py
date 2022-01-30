from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from map.models import Point
from users.factories import UserFactory


class PointTest(TestCase):

    def test_new_point_is_linked_to_request_user(self):
        user = UserFactory()
        client = Client()
        client.force_login(user)
        point_data = {
            'name': 'test_point',
            'coordinates': '10,10',
        }
        response = client.post(reverse('point-list'), point_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        point = Point.objects.get(name=point_data['name'])
        self.assertEqual(point.created_by, user)
