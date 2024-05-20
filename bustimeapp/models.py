from django.db import models
from django.forms import ValidationError


class Stop(models.Model):
    sid = models.IntegerField(unique=True)
    lat = models.FloatField()
    lng = models.FloatField()


    def __str__(self) -> str:
        return f'{self.lat} - {self.lng}'