"""
Vistas para la API de usuario.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserDataSerializer,
)
from core.models import UserData


class CreateUserView(generics.CreateAPIView):
    """Crea un nuevo usuario en el sistema."""
    serializer_class = UserSerializer


class AllUserDataView(generics.ListAPIView):
    """Lista Toda la Info de todos los Usuarios para Admins"""
    serializer_class = UserDataSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return UserData.objects.all()


class UserPersonalDataCreateView(generics.CreateAPIView):
    """Agrega la Info de Nuevos Usuarios"""
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically link the user to the UserData instance
        serializer.save()


class UserPersonalDataView(generics.RetrieveUpdateAPIView):
    """Administra la Info de los Usuarios existentes"""
    serializer_class = UserDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Normal user can interact only with their own data
        return UserData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically link the user to the UserData instance
        serializer.save(user=self.request.user)

    def get_object(self):
        """Recupera y devuelve la info del usuario"""
        return UserData.objects.get(user=self.request.user)


class CreateTokenView(ObtainAuthToken):
    """Crea un nuevo token de autenticación para usuario"""
    serializer_class = AuthTokenSerializer
    # para usar las clases de renderizado con esta view
    # es decir, para que se renderizen y sean visibles
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Administra el usuario autenticado"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Recupera y devuelve al usuario"""
        return self.request.user
