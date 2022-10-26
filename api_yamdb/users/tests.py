from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UsersManagersTests(TestCase):

    def test_create_user(self):

        user = User.objects.create_user(
            username='foo',
            email='normal@user.com',
        )
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):

        admin_user = User.objects.create_superuser(
            username='foo',
            email='super@user.com',
        )
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
