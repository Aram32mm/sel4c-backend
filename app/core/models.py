"""
Modelos de BD
"""
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    country = models.CharField(max_length=255)
    discipline = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Activity(models.Model):
    """Objeto de Actividad"""
    id = models.FloatField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class FormsQuestion(models.Model):
    """Objeto de Pregunta de Formulario """
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.question


class AcitvityResponse(models.Model):
    """Objeto de Respuesta de Actividad"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
    )
    response = models.TextField()
    time_minutes = models.IntegerField()

    def __str__(self):
        return self.response


class FormsQuestionResponse(models.Model):
    """Objeto de Respuesta a Pregunta de Formulario"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    question = models.OneToOneField(
        FormsQuestion,
        on_delete=models.CASCADE,
    )
    response = models.TextField()
    time_minutes = models.IntegerField()

    def __str__(self):
        return self.response
