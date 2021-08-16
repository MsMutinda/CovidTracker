from django.db import models


class Health(models.Model):
    id = models.AutoField(primary_key=True)
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
    risk_areas = models.CharField(max_length=50, default=None)
    crowdy_places = models.CharField(max_length=50, default=None)
    international_travel = models.CharField(max_length=250, default=None)
    victim_contact = models.CharField(max_length=250, default=None)

    class Meta:
        db_table = 'travel'