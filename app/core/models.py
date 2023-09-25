"""
Modelos de BD
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def activity_media_response_file_path(instance, filename):
    """Genera la ruta del archivo para la nueva respuesta"""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    # Determina la carpeta destino en función del tipo de archivo
    if ext in ['.jpg', '.jpeg', '.png', '.gif']:
        type = 'image'
    elif ext in ['.mp4', '.avi', '.mov']:
        type = 'video'
    elif ext in ['.wav', '.mp3', '.ogg']:
        type = 'audio'
    else:
        type = 'other'  # Otras extensiones de archivo

    return os.path.join('uploads', type, filename)


class UserManager(BaseUserManager):
    """Objeto de Manager/Admin para Usuarios """

    def create_user(self, email, password=None, **extra_fields):
        """Crea, guarda y devuelve un nuevo usuario"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Crea y devuelve un super usuario(admin)"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Objeto de Usuario Base"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)  # name as Username
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ####
    date_joined = models.DateTimeField(default=now, editable=False)
    """
    PermissionsMixin genera automáticamente los campos:
    'id','password','last_login','is_superuser','email','name', 'is_active',
    'is_staff', 'groups', 'user_permissions'

    Campos faltantes: 'date_joined'
    """
    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserData(models.Model):
    """Objeto de Información de Usuario"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_name = models.CharField(max_length=255)
    academic_degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    age = models.IntegerField()
    country = models.CharField(max_length=255)
    discipline = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class UserInitialScore(models.Model):
    """Objeto de Scores de Usuario"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    self_control_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    leadership_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    consciousness_and_social_value_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    social_innovation_and_financial_sustainability_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    systemic_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    scientific_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    critical_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    innovative_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    def __str__(self):
        return self.user.email


class UserFinalScore(models.Model):
    """Objeto de Scores de Usuario"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    self_control_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    leadership_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    consciousness_and_social_value_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    social_innovation_and_financial_sustainability_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    systemic_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    scientific_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    critical_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    innovative_thinking_score = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )

    def __str__(self):
        return self.user.email


class FormsQuestion(models.Model):
    """Objeto de Pregunta de Formulario """
    question = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.question


class FormsQuestionResponse(models.Model):
    """Objeto de Respuesta a Pregunta de Formulario"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        FormsQuestion,
        on_delete=models.CASCADE,
    )
    score = models.PositiveIntegerField()
    time_minutes = models.IntegerField()

    def __str__(self):
        return f"User: {self.user.name} - Question: {self.question.question}"  # noqa

    class Meta:
        unique_together = ('user', 'question')


class Activity(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    parent_activity = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_activities')  # noqa

    def __str__(self):
        return self.title


class ActivityResponse(models.Model):
    """Objeto de Respuesta de Actividad"""
    RESPONSE_TYPES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
    )
    response_type = models.CharField(max_length=10, choices=RESPONSE_TYPES)
    string_response = models.TextField(null=True)
    image_response = models.ImageField(null=True, upload_to=activity_media_response_file_path)  # noqa
    video_response = models.FileField(null=True, upload_to=activity_media_response_file_path)  # noqa
    audio_response = models.FileField(null=True, upload_to=activity_media_response_file_path)  # noqa
    time_minutes = models.IntegerField()

    def __str__(self):
        return f"{self.user.name} | {self.activity.title} ({self.response_type} response)"  # noqa

    class Meta:
        unique_together = ('user', 'activity')
