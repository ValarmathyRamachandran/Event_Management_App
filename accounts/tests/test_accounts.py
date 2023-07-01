from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from accounts.models import User


class TestsCasesForRegistration(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@gmail.com', password='test12345')

    def test_registration_successful(self):
        url = reverse('register')
        data = {
            "first_name": "test",
            "last_name": "name",
            "username": "testuser",
            "email": "test@gmail.com",
            "password": "test12345",
            "confirm_password": "test1234"
        }
       
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        url = reverse('login', )
        data = {
            "email": "test@gmail.com",
            "password": "test12345"
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

