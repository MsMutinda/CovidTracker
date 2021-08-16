from django.db import models


class Health(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=50, default='Female')
    age = models.CharField(max_length=50, default='18-25')
    disease = models.CharField(max_length=250, default='Asthma')
    medication = models.CharField(max_length=250, default='Yes')
    transplant = models.CharField(max_length=250, default='No')
    vaccination = models.CharField(max_length=250, default='Yes')

    class Meta:
        db_table = 'health'

    def __str__(self):
        return self.id


class Travel(models.Model):
    id = models.AutoField(primary_key=True)
    risk_areas = models.CharField(max_length=50, default='Yes')
    crowdy_places = models.CharField(max_length=50, default='No')
    international_travel = models.CharField(max_length=250, default='Yes')
    covidvictim_contact = models.CharField(max_length=250, default='No')

    class Meta:
        db_table = 'travel'

    def __str__(self):
        return self.id