from django.shortcuts import render
import requests
import json
from django.template.context_processors import csrf


def stats(request):
    resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)
    with open('resp.json', 'w') as outputfile:
        json.dump(resp, outputfile)
    with open('resp.json', 'r') as f:
        resp_file = json.load(f)
        # for val in resp_file:
            # print(val['Country'], val['Date'], val['NewConfirmed'], val['NewDeaths'], val['NewRecovered'], val['TotalConfirmed'])

    c = {'resp_file': resp_file}
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)


def health_history():
    print("Fill in details on your health history here: ")
    # html form


def travel_history():
    print("Fill in details on your travel history here: ")
    # html form

