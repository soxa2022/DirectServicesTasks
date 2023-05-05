from django.db import models
from django.utils import timezone


class WeatherInfo(models.Model):
    city = models.CharField(max_length=30, null=False)
    temperature = models.FloatField()
    humidity = models.IntegerField()
    description = models.CharField(max_length=80)
    create_at = models.DateTimeField(default=timezone.now)
