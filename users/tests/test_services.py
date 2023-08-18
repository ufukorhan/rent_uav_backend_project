from django.test import TestCase
from ..models import User
from ..services import UserService

class UserServiceTestCase(TestCase):
    def setUp(self):
        self.service = UserService()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

    def test_create_object(self):
        email = 'testuser2@example.com'
        user = self.service.create_object(email, 'testpass')
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, email)

    def test_update_object(self):
        new_email = 'newuser@example.com'
        updated_user = self.service.update_object(self.user, email=new_email)
        self.assertEqual(updated_user.email, new_email)

    def test_delete_object(self):
        self.service.delete_object(self.user)
        self.assertFalse(self.user.is_active) # is_active is set to False when a user is deleted.
