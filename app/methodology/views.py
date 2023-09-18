"""
Views para Metodologia (Actividades y Preguntas)
"""
from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.exceptions import NotFound, ValidationError

from core.models import Activity, FormsQuestion
from methodology.serializers import ActivitySerializer, FormsQuestionSerializer


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
    """Administra las Actividades (Se tiene que ser SuperAdmin)"""
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all().order_by('title')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]


class SubActivityView(generics.ListAPIView):
    """Devuelve las Sub-Activities de una Actividad Padre """
    serializer_class = ActivitySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        parent_activity_id = self.kwargs.get('parent_activity_id')

        if parent_activity_id:
            try:
                parent_activity = Activity.objects.get(pk=parent_activity_id)
                queryset = parent_activity.sub_activities.all().order_by('title')  # noqa
            except Activity.DoesNotExist:
                raise NotFound(detail="Parent activity does not exist")
        else:
            raise ValidationError("Parent activity ID is required.")

        return queryset


class FormsQuestionViewSet(viewsets.ModelViewSet):
    """Administra las Preguntas del Forms (Se tiene que ser SuperAdmin)"""
    serializer_class = FormsQuestionSerializer
    queryset = FormsQuestion.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]
