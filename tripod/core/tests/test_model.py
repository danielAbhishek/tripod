from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagersTests(TestCase):
    def test_create_user(self):
        """
        using create_user function to create user with basic
        permission levels
        """
        User = get_user_model()
        user = User.objects.create_user(email='test@gmail.com', password='foo')
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='foo')

    def test_create_superuser(self):
        """
        testing the creation of the superuser account
        """
        User = get_user_model()
        admin = User.objects.create_superuser(email='test@admin.com',
                                              password='foo')
        self.assertEqual(admin.email, 'test@admin.com')
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super@user.com',
                                          password='foo',
                                          is_superuser=False)

    def test_create_client(self):
        """
        testing the creation of the client account
        """
        User = get_user_model()
        client = User.objects.create_client(email='client@mail.com',
                                            password='abcd@1234')
        self.assertEqual(client.email, 'client@mail.com')
        self.assertTrue(client.is_active)
        self.assertTrue(client.is_client)
        self.assertFalse(client.is_staff)
        self.assertFalse(client.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_client(email='client@email.com',
                                       password='foo1234',
                                       is_staff=True)

        with self.assertRaises(ValueError):
            User.objects.create_client(email='client@email.com',
                                       password='foo1234',
                                       is_superuser=True)
