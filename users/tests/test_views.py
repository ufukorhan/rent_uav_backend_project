from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from uavs.models import UAV, RentedUAV
from model_mommy import mommy

class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(password='testpass', email='user1@example.com')
        self.superuser = User.objects.create_superuser(password='testpass', email='superuser@example.com')
        self.valid_payload = {'password': 'testpass', 'email': 'user2@example.com'}
        self.invalid_payload = {'password': '', 'email': 'user2@example.com'}

    def test_list_users(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 2)
        self.assertEqual(User.objects.count(), 2)

    def test_create_valid_user(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post('/api/v1/users/', data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertTrue(User.objects.filter(email='user2@example.com').exists())

    def test_create_invalid_user(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post('/api/v1/users/', data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.json().get('password'), ['This field may not be blank.'])

    def test_retrieve_user(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user1@example.com')
        self.assertEqual(response.json().get('id'), str(self.user.id))

    def test_update_user(self):
        self.client.force_authenticate(user=self.superuser)
        payload = {'password': 'testpass', 'email': 'user_updated_mail@example.com'}
        response = self.client.put(f'/api/v1/users/{self.user.id}/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=self.user.id).email, 'user_updated_mail@example.com')
        self.assertEqual(response.json().get('email'), "user_updated_mail@example.com")

    def test_delete_user(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(f'/api/v1/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_me(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user1@example.com')
        self.assertEqual(response.json().get('id'), str(self.user.id))

    def test_rental_records(self):
        self.client.force_authenticate(user=self.user)
        RentedUAV.objects.create(user=self.user, uav=mommy.make(UAV), start_date='2021-01-01', end_date='2021-01-02')
        response = self.client.get('/api/v1/users/me/rental-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 1)

    def test_rental_records_no_records(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/users/me/rental-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), 0)