from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserAuthenticationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('api_register') 
        self.login_url = reverse('api_login')        
        self.user_data = {
            'username': 'rasha001',
            'email': 'asad@gmail.com',
            'password': 'GRsupra3.0'
        }

    def test_user_registration(self):
        #Test registering a new user.
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_existing_username(self):
        #Test registering with an existing username.
        User.objects.create_user(username='rasha001', password='GRsupra3.0')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_user_login(self):
        #Test logging in with valid credentials.
        User.objects.create_user(username='testuser', password='password123')
        login_data = {
            'username': 'rasha001',
            'password': 'GRsupra3.0'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_login_invalid_credentials(self):
        #Test logging in with invalid credentials.
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)