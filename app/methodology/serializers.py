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


class FormsQuestionSerializer(serializers.ModelSerializer):
    """Serializer para Pregunta de Forms"""

    class Meta:
        model = FormsQuestion
        fields = '__all__'
        read_only_fields = ['id']
