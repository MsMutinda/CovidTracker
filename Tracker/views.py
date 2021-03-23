from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from django.template.context_processors import csrf
from django import template


def stats(request):
    resp = requests.get('https://api.covid19api.com/country/ke').json()
    # resp_data = json.loads(resp)

    c = {'resp': resp}
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)

