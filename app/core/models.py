"""
Modelos de BD
"""
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager para usuarios """

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
    """Usuario base"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)  # name as Username
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ####
    date_joined = models.DateTimeField(default=now, editable=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    """
    PermissionsMixin genera automáticamente los campos:
    'id','password','last_login','is_superuser','email','name', 'is_active',
    'is_staff', 'groups', 'user_permissions'

    Campos faltantes: 'first_name', 'last_name', 'date_joined'
    """
    objects = UserManager()

    USERNAME_FIELD = 'email'
