from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Health(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=5)
    is_active = models.BooleanField(default=None)
    gender = models.CharField(max_length=50, default=None)
    age = models.CharField(max_length=50, default=None)
    diseases = models.TextField(max_length=250, default=None)
    medication = models.CharField(max_length=250, default=None)
    transplant = models.CharField(max_length=250, default=None)
    vaccination = models.CharField(max_length=250, default=None)

    class Meta:
        db_table = 'health'


class Travel(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=5)
    is_active = models.BooleanField(default=None)
    risk_areas = models.CharField(max_length=50, default=None)
    crowdy_places = models.CharField(max_length=50, default=None)
    international_travel = models.CharField(max_length=250, default=None)
    victim_contact = models.CharField(max_length=250, default=None)

    class Meta:
        db_table = 'travel'