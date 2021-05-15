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
