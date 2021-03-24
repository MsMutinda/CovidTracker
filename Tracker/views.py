from django.shortcuts import render
import requests
import json
from Tracker.models import GetData
from django.template.context_processors import csrf


def stats(request):
    # resp_data = GetData.objects.all()
    with open('resp.json', 'r') as f:
        resp_file = json.load(f)
    c = {
         'resp_data': GetData.objects.all(),
         'resp_file': resp_file
        }
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)


def health_history():
    print("Fill in details on your health history here: ")
    # html form


def travel_history():
    print("Fill in details on your travel history here: ")
    # html form

