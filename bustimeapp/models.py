from django.db import models
from django.forms import ValidationError
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class Stop(models.Model):
    sid = models.IntegerField(unique=True)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self) -> str:
        return f"{self.lat} - {self.lng}"
    
class BusSchedule(models.Model):
    tipo_dia = models.IntegerField()
    cod_variante = models.IntegerField()
    frecuencia = models.IntegerField()
    cod_ubic_parada = models.IntegerField()
    ordinal = models.IntegerField()
    hora = models.IntegerField()
    dia_anterior = models.CharField()

    def __str__(self) -> str:
        return self.id

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    favourite_stops = models.ManyToManyField("Stop")

    objects = UserManager()

    USERNAME_FIELD = "email"
