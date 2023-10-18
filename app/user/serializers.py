"""
Serializers para el la Vista de API usuario
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers
from core.models import UserData, UserInitialScore, UserFinalScore


class UserSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de usuario."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'is_staff', 'is_superuser']
        read_only_fields = ['is_staff', 'is_superuser']
        # no se puede leer una contraseña, el largo mínimo es 5
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Crea y devuelve un usuario con contraseña cifrada"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Actualiza y devuelve usuario"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDataSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de información de usuario"""
    class Meta:
        model = UserData
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserData.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserInitialScoreSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de scores iniciales de usuario"""
    class Meta:
        model = UserInitialScore
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserInitialScore.objects.create(user=user, **validated_data)


class UserFinalScoreSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de scores finales de usuario"""
    class Meta:
        model = UserFinalScore
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        return UserFinalScore.objects.create(user=user, **validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializador para el token de autenticación del usuario"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):  # attrs as attributes
        """Valida y autentica al usuario"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(  # funcion django de autenticación
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
