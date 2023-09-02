"""
Tests para modelos
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Testeo de Modelos"""

    def test_create_user_successful(self):
        """Test creando un usuario exitoso """
        email = 'test@example.com'
        password = 'testpass123'
        name = "Test"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test de email normalizado"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test de error al no pasar email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creando un superusuario"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_add_user_info(self):
        """Test agregando información del Usuario"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name="Test",
        )
        data = models.UserData.objects.create(
            user=user,
            full_name='Full name Test',
            academic_degree='Academic Degree',
            institution='SEL4C',
            gender='Male',
            birthday='2023-09-15',
            country='Mexico',
            discipline='STEM',
        )

        self.assertEqual(str(data), data.full_name)

    def test_create_activity(self):
        """Test creando una actividad"""
        activity = models.Activity.objects.create(
            id=1.1,
            title='Sample activity name ',
            description='Sample activity description.',
        )

        self.assertEqual(str(activity), activity.title)

    def test_create_forms_question(self):
        """Test creando una pregunta del forms """
        formsquestion = models.FormsQuestion.objects.create(
            question='Sample forms question?',
            description='Sample forms question',
        )

        self.assertEqual(str(formsquestion), formsquestion.question)

    def test_activity_response(self):
        """Test respondiendo una actividad"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        activity = models.Activity.objects.create(
            id=1.1,
            title='Sample activity name ',
            description='Sample activity description.',
        )
        activity_response = models.AcitvityResponse.objects.create(
            user=user,
            activity=activity,
            response='Response',
            time_minutes=5,
        )

        self.assertEqual(str(activity_response), activity_response.response)

    def test_forms_question_response(self):
        """Test respondiendo una pregunta del forms"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        formsquestion = models.FormsQuestion.objects.create(
            question='Sample forms question?',
            description='Sample forms question',
        )
        formquestion_response = models.FormsQuestionResponse.objects.create(
            user=user,
            question=formsquestion,
            response='Response',
            time_minutes=5,
        )

        self.assertEqual(str(formquestion_response), formquestion_response.response)  # noqa
