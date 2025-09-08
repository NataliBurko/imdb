from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class RegisterTestCase(APITestCase):

    def test_register(self):
        data ={
            "username": "testcase",
            "email": "testcase@test.com",
            "password": "testcase"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example",
                                        password="example123")
        
    def test_login(self):
        data = {
            "username": "example",
            "password": "example123"

        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        login_resp = self.client.post(reverse('login'), {
            "username": "example",
            "password": "example123"
        })
        token = login_resp.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token '+ token)
        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
