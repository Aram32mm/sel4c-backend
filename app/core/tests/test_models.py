"""
Tests for models.
"""
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        # id
        email = 'test@example.com'
        name = 'Testeo'
        is_active = True
        is_staff = False
        is_superuser = False
        password = 'testpass123'
        last_login = datetime(2023, 8, 30, 18, 0)
        date_joined = datetime(2023, 8, 30, 18, 0)

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name = name,
            is_active = is_active,
            is_staff = is_staff,
            is_superuser = is_superuser,
            last_login = last_login,
            date_joined = date_joined,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.name, name)
        self.assertEqual(user.is_active, is_active)
        self.assertEqual(user.is_staff, is_staff)
        self.assertEqual(user.is_superuser, is_superuser)
        self.assertEqual(user.last_login, last_login)
        self.assertEqual(user.date_joined, date_joined)

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)
