"""
Serializers para Metodologia (Actividades y Preguntas)
"""
from rest_framework import serializers

from core.models import (
    Activity,
    FormsQuestion
)


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer para Actividad"""

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        return Activity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FormsQuestionSerializer(serializers.ModelSerializer):
    """Serializer para Pregunta de Forms"""

    class Meta:
        model = FormsQuestion
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        return FormsQuestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
