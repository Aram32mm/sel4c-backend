"""
Serializers para el la Vista de API usuario
"""
import hashlib
import logging
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework.authtoken.models import Token
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

    def create_auth_token(self, user):
        """
        Crea y Actualiza un Token
        """
        try:
            token = Token.objects.filter(user=user)
            if not token:
                token = Token.objects.get_or_create(user=user)
            else:
                token = Token.objects.filter(user=user)
                new_key = token[0].generate_key()

                # Cifra una cadena aleatoria usando SHA1
                sha1_algorithm = hashlib.sha1()
                sha1_algorithm.update(new_key.encode('utf-8'))
                first_level_value = sha1_algorithm.hexdigest()

                # Cifra una cadena aleatoria usando MD5
                md5_algorithm = hashlib.md5()
                md5_algorithm.update(first_level_value.encode('utf-8'))
                second_level_value = md5_algorithm.hexdigest()

                token.update(key=second_level_value)
            return token
        except Exception as ex:
            logging.error(msg=f'Failed to create auth token {ex}', stacklevel=logging.CRITICAL)  #
            pass

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

        self.create_auth_token(user)
        attrs['user'] = user
        return attrs
