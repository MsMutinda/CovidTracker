from django.db import models
# from django.http import HttpResponse


# Create your models here.
class DataMap(models.Model):
    label = ['World statistics']

    # world map

    # options to filter display to be country-based
    # def data_filter:
    filtered = models.CharField(max_length=50, help_text='Filter data', default='Filter results')


class Health(models.Model):
    # return HttpResponse('Enter details on your health history here')
    healthqn1 = models.CharField(max_length=50)
    healthqn2 = models.CharField(max_length=50)
    healthqn3 = models.CharField(max_length=50)


class Travel(models.Model):
    travelqn1 = models.CharField(max_length=50)
    travelqn2 = models.CharField(max_length=50)
    travelqn3 = models.CharField(max_length=50)


class Feedback(models.Model):
    choice1 = models.TextField(max_length=250)
    choice2 = models.TextField(max_length=250)
    choice3 = models.TextField(max_length=250)
