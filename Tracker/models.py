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
    print('Filter based on location')
    # filtered = models.CharField(max_length=20, help_text='Filter data', choices=stats.df_obj, default='Filter results')


class Health(models.Model):
    # return HttpResponse('Enter details on your health history here')
    healthqn1 = models.CharField(max_length=150, default='Question 1')
    healthqn2 = models.CharField(max_length=150, default='Question 2')
    healthqn3 = models.CharField(max_length=150, default='Question 3')
    healthqn4 = models.CharField(max_length=150, default='Question 4')


class Travel(models.Model):
    travelqn1 = models.CharField(max_length=150, default='Question 1')
    travelqn2 = models.CharField(max_length=150, default='Question 2')
    travelqn3 = models.CharField(max_length=150, default='Question 3')
    travelqn4 = models.CharField(max_length=150, default='Question 4')
