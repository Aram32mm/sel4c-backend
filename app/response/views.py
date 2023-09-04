"""
Views para Respuestas de Usuarios a Actividades y Preguntas
"""
from rest_framework import viewsets, generics
from core.models import ActivityResponse, FormsQuestionResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from response.serializers import (
    ActivityResponseSerializer,
    FormsQuestionResponseSerializer,
)

class AllActivitiesResponsesView(generics.ListAPIView):
    """Lista Toda la Info de todos los Usuarios para Admins (Requiere Autenticación)"""  # noqa
    serializer_class = ActivityResponseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ActivityResponse.objects.all().order_by('user_id')

class AllFormsQuestionResponsesView(generics.ListAPIView):
    """Lista Toda la Info de todos los Usuarios para Admins (Requiere Autenticación)"""  # noqa
    serializer_class = FormsQuestionResponseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return FormsQuestionResponse.objects.all().order_by('user_id')


class ActivityResponseViewSet(viewsets.ModelViewSet):
    serializer_class = ActivityResponseSerializer
    queryset = ActivityResponse.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('activity_id')

class FormsQuestionResponseViewSet(viewsets.ModelViewSet):
    serializer_class = FormsQuestionResponseSerializer
    queryset = FormsQuestionResponse.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('question_id')
