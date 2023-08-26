"""
Serializers para el la Vista de API usuario
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializador para el objeto de usuario."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'first_name', "last_name"]
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