from django.http import HttpResponse
import requests
import json


# Create your views here.
def index(request):
    return HttpResponse('Get the latest covid-19 statistics and exposure predictions here')


def stats(request):
    # resp = requests.request('GET', url='https://api.covid19api.com')
    resp = requests.get('https://api.covid19api.com/summary')
    # resp_data = json.loads(resp)
    # resp_data = resp.json()

    return HttpResponse(resp)

