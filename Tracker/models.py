from django.db import models
import json
import requests

resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)


class GetData(models.Model):
    # def __init__(self, jdata):
    # self.__dict__ = json.loads(jdata)

    with open('resp.json', 'w') as outputfile:
        json.dump(resp, outputfile)
        # for val in resp_file:
        # print(val['Country'], val['Date'], val['NewConfirmed'], val['NewDeaths'], val['NewRecovered'], val['TotalConfirmed'])


# data_object = GetData(JSONData)
# print(data_object)


class Tabular(models.Model):
    data_table = ''


class DataMap(models.Model):
    # visualize data on world map
    data_label = ['Infection statistics']
    map_label = ['Country map']


# options to filter display to be country-based
class DataFilter(models.Model):
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


class Result(models.Model):
    choice1 = models.TextField(max_length=250)
    choice2 = models.TextField(max_length=250)
    choice3 = models.TextField(max_length=250)
