"""
Vistas para la API de usuario.
"""
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserDataSerializer,
    UserInitialScoreSerializer,
    UserFinalScoreSerializer
)
from core.models import UserData, UserInitialScore, UserFinalScore


class IsSuperUser(permissions.BasePermission):
    """
    Permiso personalizado para permitir que los superusuarios
    puedan crear otros superusuarios
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class CreateUserView(generics.CreateAPIView):
    """Crea un nuevo usuario en el sistema (No requiere Autenticación)"""
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(is_staff=False, is_superuser=False)


class CreateAdminView(generics.CreateAPIView):
    """Crea un nuevo usuario en el sistema (No requiere Autenticación)"""
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)


class UserPersonalDataCreateView(generics.CreateAPIView):
    """Agrega la Info de Nuevos Usuarios (Requiere Autenticación)"""
    serializer_class = UserDataSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsSuperUser])
def users_info(request):
    """Devuelve toda la información de los usuarios (Requiere Autenticación)"""
    user_data = UserData.objects.filter(user__is_superuser=False)

    combined_data = []

    for user_data_item in user_data:

        combined_item = {
            # Campos de Usuario
            'user': user_data_item.user.pk,
            'name': user_data_item.user.name,
            'email': user_data_item.user.email,
            'is_active': user_data_item.user.is_active,
            # Campos de Datos de Usuarios
            'full_name': user_data_item.full_name,
            'academic_degree': user_data_item.academic_degree,
            'institution': user_data_item.institution,
            'gender': user_data_item.gender,
            'age': user_data_item.age,
            'country': user_data_item.country,
            'discipline': user_data_item.discipline,
        }

        initial_score = UserInitialScore.objects.filter(user=user_data_item.user).first()  # noqa
        if initial_score:
            combined_item['initial_score'] = UserInitialScoreSerializer(initial_score).data  # noqa
        else:
            combined_item['initial_score'] = 0  # Default value

        final_score =  UserFinalScore.objects.filter(user=user_data_item.user).first()  # noqa
        if final_score:
            combined_item['final_score'] = UserFinalScoreSerializer(final_score).data  # noqa
        else:
            combined_item['final_score'] = 0  # Default value

        combined_data.append(combined_item)

    return Response(combined_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsSuperUser])
def admins_info(request):
    """Devuelve toda la información de los admins (Requiere Autenticación)"""
    user_data = get_user_model().objects.filter(is_superuser=True)

    combined_data = []

    for user_data_item in user_data:

        combined_item = {
            # Campos de Usuario
            'user': user_data_item.pk,
            'name': user_data_item.name,
            'email': user_data_item.email,
            'is_active': user_data_item.is_active
        }

        combined_data.append(combined_item)

    return Response(combined_data)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsSuperUser])
def deactivate_user(request, user_id):
    """Desactiva a un usuario (Requiere Autenticación)"""
    user = get_object_or_404(get_user_model(), id=user_id)
    user.is_active = False
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


class UserInitialScorePostView(generics.ListCreateAPIView):
    """Maneja los scores iniciales de Usuario (Requiere Autenticación)"""
    serializer_class = UserInitialScoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        is_admin = self.request.user.is_superuser

        if is_admin:
            queryset = UserInitialScore.objects.all().order_by('user__id')
        else:
            queryset = UserInitialScore.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class UserFinalScorePostView(generics.ListCreateAPIView):
    """Maneja los scores finales de Usuario (Requiere Autenticación)"""
    serializer_class = UserFinalScoreSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        is_admin = self.request.user.is_superuser

        if is_admin:
            queryset = UserFinalScore.objects.all().order_by('user__id')
        else:
            queryset = UserFinalScore.objects.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class CreateTokenView(ObtainAuthToken):
    """Crea un nuevo token de autenticación para usuario (No requiere Autenticación)"""  # noqa
    serializer_class = AuthTokenSerializer
    # para usar las clases de renderizado con esta view
    # es decir, para que se renderizen y sean visibles
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Administra el usuario autenticado (Requiere Autenticación)"""
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Recupera y devuelve al usuario"""
        return self.request.user
