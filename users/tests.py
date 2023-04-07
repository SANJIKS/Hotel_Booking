from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

from users.models import OwnerRequest

User = get_user_model()

class RegistrationTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_registration(self):
        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'password_confirm': 'password123'
        }
        response = self.client.post('/account/registration/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Thanks for registration!'})
        self.assertTrue(User.objects.filter(email='test@example.com').exists())



class ActivationTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='password123')
        self.user.activation_code = 'testcode'
        self.user.save()

    def test_activation_success(self):
        data = {'activation_code': 'testcode'}
        response = self.client.post('/account/activation/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'message': 'Аккаунт успешно активирован!'})
        user = User.objects.get(email='test@example.com')
        self.assertTrue(user.is_active)
        self.assertEqual(user.activation_code, '')




class ActivationFailTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_activation_invalid_code(self):
        user = User.objects.create_user(email='test@example.com', password='password123')
        user.activation_code = '123456'
        user.save()
        
        data = {'activation_code': 'wrong_code'}
        response = self.client.post('/account/activation/', data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'activation_code': ['Неверно указан код']})




class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_login(self):
        user = User.objects.create_user(email='test@example.com', password='password123')
        
        data = {'email': 'test@example.com', 'password': 'wrong_password'}
        response = self.client.post('/account/login/', data)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'non_field_errors': ['Неправильно указан email или пароль']})



class LogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com', password='test_password')
        self.token = Token.objects.create(user=self.user)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete('/account/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())


class OwnerRequestCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@gmail.com',
            password='testpass'
        )
        self.client.login(email='testuser@gmail.com', password='testpass')

    def test_create_owner_request(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('owner-create')
        data = {'message': 'Test owner request message.'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OwnerRequest.objects.count(), 1)
        self.assertEqual(OwnerRequest.objects.get().message, 'Test owner request message.')
        self.assertEqual(OwnerRequest.objects.get().user, self.user)