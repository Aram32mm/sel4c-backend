"""
Serializers para Respuestas de Usuarios a Actividades y Preguntas
"""
from rest_framework import serializers

from core.models import (
    ActivityResponse,
    FormsQuestionResponse
)

class ActivityResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityResponse
        fields = '__all__'
        read_only_fields = ['user', 'activity']

class FormsQuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsQuestionResponse
        fields = '__all__'
        read_only_fields = ['user', 'question']