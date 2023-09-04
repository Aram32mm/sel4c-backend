"""
Vistas para la API de usuario.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserDataSerializer,
)
from core.models import UserData


class CreateUserView(generics.CreateAPIView):
    """Crea un nuevo usuario en el sistema (No requiere Autenticación)"""
    serializer_class = UserSerializer


class AllUserDataView(generics.ListAPIView):
    """Lista Toda la Info de todos los Usuarios para Admins (Requiere Autenticación)"""  # noqa
    serializer_class = UserDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return UserData.objects.all()


class UserPersonalDataCreateView(generics.CreateAPIView):
    """Agrega la Info de Nuevos Usuarios (Requiere Autenticación)"""
    serializer_class = UserDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically link the user to the UserData instance
        serializer.save()


class UserPersonalDataView(generics.RetrieveUpdateAPIView):
    """Administra la Info de los Usuarios existentes (Requiere Autenticación)"""  # noqa
    serializer_class = UserDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserData.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        return UserData.objects.get(user=self.request.user)


class CreateTokenView(ObtainAuthToken):
    """Crea un nuevo token de autenticación para usuario (No requiere Autenticación)"""  # noqa
    serializer_class = AuthTokenSerializer
    # para usar las clases de renderizado con esta view
    # es decir, para que se renderizen y sean visibles
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Administra el usuario autenticado (Requiere Autenticación)"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Recupera y devuelve al usuario"""
        return self.request.user
