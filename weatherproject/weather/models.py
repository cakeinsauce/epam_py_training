from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Weather(models.Model):
    time = models.DateTimeField(primary_key=True)
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
        managed = False


class Forecast(models.Model):
    reception_time = models.DateTimeField()
    location = models.JSONField(primary_key=True)
    units = models.CharField(max_length=11)
    forecasts = ArrayField(models.JSONField())

    def __str__(self):
        return f"{self.reception_time} {self.location} {self.units} {self.forecasts}"

    class Meta:
        managed = False
        unique_together = ("reception_time", "location")


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["username"]

    # objects = AccountManager()

    def __str__(self):
        return self.username
