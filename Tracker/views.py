from django.shortcuts import render
from .models import GetData as GetDataModel
from django.template.context_processors import csrf
import json


def stats(request):
    # resp_data = GetData.objects.all()
    with open('resp.json', 'r') as f:
        respfile = json.load(f)
    c = {
        'resp_data': GetDataModel.objects.all(),
        'respfile': respfile
        }
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)


def health_history(request):
    print("Fill in details on your health history here: ")
    # html form


def travel_history(request):
    print("Fill in details on your travel history here: ")
    # html form

