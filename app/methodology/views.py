"""
Views para Metodologia (Actividades y Preguntas)
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

from core.models import (
    Activity,
    FormsQuestion,
)
from methodology import serializers


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que los superusuarios tengan
    acceso completo y acceso de sólo lectura para otros usuarios.
    """

    def has_permission(self, request, view):
        # Allow read-only access to all users (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow full access to superusers
        return request.user.is_superuser


class ActivityViewSet(viewsets.ModelViewSet):
    """View para manejar APIs de Actividad"""
    serializer_class = serializers.ActivitySerializer
    queryset = Activity.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        """Recupera Actividades para Usuario Autenticado"""
        return self.queryset.order_by('id')

    def perform_create(self, serializer):
        """Crea nueva actividad"""
        serializer.save()


class FormsQuestionViewSet(viewsets.ModelViewSet):
    """View para manejar APIs de Pregunta de Forms"""
    serializer_class = serializers.FormsQuestionSerializer
    queryset = FormsQuestion.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        """Recupera Preguntas del Forms para Usuario Autenticado"""
        return self.queryset.order_by('id')

    def perform_create(self, serializer):
        """Crea nueva pregunta de forms """
        serializer.save()
