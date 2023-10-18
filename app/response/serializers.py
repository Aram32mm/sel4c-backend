"""
Serializers para Respuestas de Usuarios a Actividades y Preguntas
"""
from rest_framework import serializers

from core.models import (
    ActivityResponse,
    FormsQuestionResponse,
    ModuleResponseCompletion
)


class ModuleResponseCompletionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo de de finalización de resouesta de un módulo"""  # noqa
    class Meta:
        model = ModuleResponseCompletion
        fields = '__all__'
        read_only_fields = ['id', 'user', 'parent_activity']

    def create(self, validated_data):
        return ModuleResponseCompletion.objects.create(**validated_data)


class ActivityResponseSerializer(serializers.ModelSerializer):
    """Serializador para ver Actividades y sus Respuestas"""
    class Meta:
        model = ActivityResponse
        fields = ['id', 'user', 'activity', 'response_type', 'string_response', 'image_response', 'video_response', 'audio_response', 'time_minutes']  # noqa
        read_only_fields = ['id', 'user', 'activity']

    def validate(self, data):
        response_type = data.get('response_type')
        if response_type == 'text':
            if not data.get('string_response'):
                raise serializers.ValidationError("a string response is required for text response.")  # noqa
            data.pop('image_response', None)
            data.pop('video_response', None)
            data.pop('audio_response', None)
        elif response_type == 'image':
            if not data.get('image_response'):
                raise serializers.ValidationError("an image response is required for image response.")  # noqa
            data.pop('string_response', None)
            data.pop('video_response', None)
            data.pop('audio_response', None)
        elif response_type == 'video':
            if not data.get('video_response'):
                raise serializers.ValidationError("a video response is required for video response.")  # noqa
            data.pop('string_response', None)
            data.pop('image_response', None)
            data.pop('audio_response', None)
        elif response_type == 'audio':
            if not data.get('audio_response'):
                raise serializers.ValidationError("an audio response is required for audio response.")  # noqa
            data.pop('string_response', None)
            data.pop('image_response', None)
            data.pop('video_response', None)
        else:
            raise serializers.ValidationError("Invalid response_type.")

        return data

    def create(self, validated_data):
        return ActivityResponse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FormsQuestionResponseSerializer(serializers.ModelSerializer):
    """Serializador para respuestas de forms"""
    class Meta:
        model = FormsQuestionResponse
        fields = '__all__'
        read_only_fields = ['user', 'question']

    def create(self, validated_data):
        return FormsQuestionResponse.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
