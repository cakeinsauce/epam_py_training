from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Weather(models.Model):
    """Weather model"""

    time = models.DateTimeField()
    status = models.CharField(max_length=20)
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    direction = models.CharField(max_length=3)
    humidity = models.IntegerField()
    rain = models.FloatField()
    snow = models.FloatField()

    def __str__(self):
        return f"{self.time} {self.status} {self.temperature}"

    class Meta:
        # managed = True
        ordering = ["time"]


class Forecast(models.Model):
    """City forecast model."""

    reception_time = models.DateTimeField()
    location = models.JSONField()
    unit = models.CharField(max_length=11)
    forecasts = models.ManyToManyField(Weather, related_name="weather")

    def __str__(self):
        return f"{self.reception_time} {self.location} {self.unit} {self.forecasts}"

    class Meta:
        # managed = True
        ordering = ["reception_time"]


class AccountManager(BaseUserManager):
    """Custom user account manager"""

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    """Custom user account model."""

    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = AccountManager()

    def __str__(self):
        return self.username

    # For checking permissions.
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Create auth token of user when register."""
    if created:
        Token.objects.create(user=instance)
