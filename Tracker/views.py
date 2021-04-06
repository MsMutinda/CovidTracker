from django.shortcuts import render
# from .models import GetData as GetDataModel
from django.template.context_processors import csrf
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
            global respdata
            respdata = respdata1[item]
    # print(*respdata, sep='\n')
        df_old = pd.DataFrame(respdata)
        df = df_old.drop(columns=["Premium", "Slug", "ID"])
        df_obj = df.to_html(classes='mystyle')

        # df_obj = df.to_html(index=False)
    # with open('resp.json', 'r') as f:
    #     respfile = json.load(f)
    c = {
        # 'resp_data': GetDataModel.objects.all(),
        'respdata1': respdata1,
        'df_obj': df_obj
        }
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)


def health_history(request):
    print("Fill in details on your health history here: ")
    # html form


def travel_history(request):
    print("Fill in details on your travel history here: ")
    # html form
