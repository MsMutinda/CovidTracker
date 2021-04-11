from django.shortcuts import render
from Tracker.models import *
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import bs4 as beauty
import json
import requests
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')


def stats(request):
    resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)
    respdata1 = json.loads(resp)
    for item in respdata1.keys():
        if item == 'Countries':
            respdata = respdata1[item]
    # print(*respdata, sep='\n')
            df_old = pd.DataFrame(respdata)
            df = df_old.drop(columns=["Premium", "Slug", "ID"])
            df_obj = df.to_html(classes='mystyle', index=False)
            request.session['df_obj'] = df_obj

    c = {
        # 'resp_data': GetDataModel.objects.all(),
        'respdata1': respdata1,
        'df_obj': df_obj
        }
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)


def show_map(request):
    print("This is global map showing world infection rates")


@csrf_exempt
def filter_country(request):
    model = DataFilter
    template = '/home.html'
    df_obj = request.session.get('df_obj')
    bs = beauty(open(df_obj))  # parse the data as a string
    for row in bs.find_all('tr'):
        for tabledata in row.find_all('td'):
            searchvalue = request.POST['search_item'].get()
            if tabledata.text == searchvalue:
                data = tabledata.text
                request.session['data'] = data


@csrf_exempt
def health_history(request):
    # html form
    data = request.session.get('data')
    c = {
        'data': data
    }
    c.update(csrf(request))
    return render(request, 'Tracker/health.html', c)


def travel_history(request):
    # html form
    c = {

    }
    c.update(csrf(request))
    return render(request, 'Tracker/travel.html', c)
