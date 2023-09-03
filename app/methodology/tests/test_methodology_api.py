"""
Tests for recipe APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Activity,
    FormsQuestion,
)

from methodology.serializers import (
    ActivitySerializer,
    FormsQuestionSerializer,
)


ACTIVITIES_URL = reverse('methodology:activity-list')
FORMSQUESTIONS_URL = reverse('methodology:formsquestion-list')


def create_activity(**params):
    """Crear y devolver una actividad de muestra"""
    defaults = {
        'title': 'Sample Activity',
        'description': 'Sample description',
    }
    defaults.update(params)

    activity = Activity.objects.create(**defaults)
    return activity


def create_forms_question(**params):
    """Crear y devolver una actividad de muestra"""
    defaults = {
        'question': 'Sample question?',
        'description': 'Sample description',
    }
    defaults.update(params)

    question = FormsQuestion.objects.create(**defaults)
    return question


class PublicRecipeAPITests(TestCase):
    """Test de solicitudes API no autenticadas."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Todos pueden llamar a la API."""
        res = self.client.get(ACTIVITIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateRecipeApiTests(TestCase):
    """Test de solicitudes API autenticadas"""

    def setUp(self):
        self.client = APIClient()
        self.superuser = get_user_model().objects.create_user(
            'user@example.com',
            'test123',
        )
        self.superuser.is_superuser = True
        self.superuser.save()
        self.client.force_authenticate(self.superuser)

    def test_retrieve_activities(self):
        """Test recuperando una lista de actividades"""
        create_activity(
            title='Sample Activity 1',
            description='Sample description 1',
        )
        create_activity(
            title='Sample Activity 2',
            description='Sample description 2',
        )

        res = self.client.get(ACTIVITIES_URL)

        activities = Activity.objects.all().order_by('id')
        serializer = ActivitySerializer(activities, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_forms_questions(self):
        """Test recuperando una lista de actividades"""
        create_forms_question(
            question='Sample question 1?',
            description='Sample description 1',
        )
        create_forms_question(
            question='Sample question 2?',
            description='Sample description 2',
        )

        res = self.client.get(FORMSQUESTIONS_URL)

        formsQuestions = FormsQuestion.objects.all().order_by('id')
        serializer = FormsQuestionSerializer(formsQuestions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_activity(self):
        """Test creando una actividad"""
        payload = {
            'title': 'Sample Activity',
            'description': 'Sample description',
        }

        res = self.client.post(ACTIVITIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_forms_question(self):
        """Test creando una pregunta del forms """
        payload = {
            'question': 'Sample question?',
            'description': 'Sample description',
        }

        res = self.client.post(FORMSQUESTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    """
    Faltan tests de:
    actualizado parcial,
    actualizado total,
    de borrar y
    de permisos.
    """
