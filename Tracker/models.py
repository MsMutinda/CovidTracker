from django.db import models
from Tracker.views import stats
# import json
# import requests


# class GetData(models.Model):
#     resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)
#     with open('resp.json', 'w') as outputfile:
#         json.dump(resp, outputfile)


class DataMap(models.Model):
    # visualize data on world map
    data_label = ['Infection statistics']
    map_label = ['Country map']


# options to filter display to be country-based
class DataFilter(models.Model):
    view = stats
    # filtered = models.CharField(max_length=20, help_text='Filter data', choices=stats.df_obj, default='Filter results')


class Health(models.Model):
    # return HttpResponse('Enter details on your health history here')
    healthqn1 = models.CharField(max_length=50)
    healthqn2 = models.CharField(max_length=50)
    healthqn3 = models.CharField(max_length=50)


class Travel(models.Model):
    travelqn1 = models.CharField(max_length=50)
    travelqn2 = models.CharField(max_length=50)
    travelqn3 = models.CharField(max_length=50)


class Result(models.Model):
    choice1 = models.TextField(max_length=250)
    choice2 = models.TextField(max_length=250)
    choice3 = models.TextField(max_length=250)
