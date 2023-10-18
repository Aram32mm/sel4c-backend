"""
Vistas para la API de Swift Connection
"""
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from swiftcon.serializers import (
    UserUserDefaultsSerializer
)
from core.models import (
    # UserPhotoMedia,
    # UserVideoMedia,
    UserUserDefaults
)


class CreateUserUserDefaultsView(generics.CreateAPIView):
    """Vista para la creación del modelo de user defaults"""
    serializer_class = UserUserDefaultsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateUserUserDefaultsView(generics.RetrieveUpdateAPIView):
    """Vista para la obtención y actualización del modelo de user defaults"""
    serializer_class = UserUserDefaultsSerializer
    queryset = UserUserDefaults.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserUserDefaults.objects.get(user=self.request.user)
