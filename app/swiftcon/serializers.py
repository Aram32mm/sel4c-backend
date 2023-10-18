"""
Serializadores para la API de Swift Connection.
"""
from rest_framework import serializers
from core.models import (
    # UserPhotoMedia,
    # UserVideoMedia,
    UserUserDefaults
)


class UserUserDefaultsSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de de finalización de resouesta de un módulo"""  # noqa
    class Meta:
        model = UserUserDefaults
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        return UserUserDefaults.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
