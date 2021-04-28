from django.shortcuts import render
from Tracker.models import *
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import json
from bs4 import BeautifulSoup as beauty
import requests
from six.moves import urllib
import pandas as pd
from plotly.graph_objs import Bar
from plotly import offline
# from django.template.loader import render_to_string
pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')


def stats(request):
    resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)
    respdata1 = json.loads(resp)
    # Global stats visualization
    plotsdata = {
        'Date': respdata1['Global']['Date'],
        'New Confirmed Cases': respdata1['Global']['NewConfirmed'],
        'New Deaths': respdata1['Global']['NewDeaths'],
        'New Recoveries': respdata1['Global']['NewRecovered'],
        'Total Confirmed': respdata1['Global']['TotalConfirmed'],
        'Total Deaths': respdata1['Global']['TotalDeaths'],
        'Total Recovered': respdata1['Global']['TotalRecovered']
    }
    xdata = []
    ydata = []
    for key in plotsdata:
        xdata.append(key)
        ydata.append(plotsdata[key])
    dataplot = [{'type': 'bar', 'x': xdata, 'y': ydata}]
    plotlayout = {'title': 'Global Statistics', 'xaxis': {'title': 'Case categories'},
                  'yaxis': {'title': 'Number of cases'}}
    fig = {'data': dataplot, 'layout': plotlayout}
    figplot = offline.plot(fig, filename='globstats.html')
    graph = figplot.to_html(full_html=False, default_height=500, default_width=400)
    # test = render_to_string('globstats.html')

    # Data per country
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
        'df_obj': df_obj,
        # 'figplot': figplot
        'graph': graph
    }
    c.update(csrf(request))
    return render(request, 'Tracker/home.html', c)


@csrf_exempt
def filter_country(request):
    # model = DataFilter
    template = '/home.html'
    df_obj = request.session.get('df_obj')
    bs = beauty(open(df_obj))  # parse the data as a string
    for row in bs.find_all('tr'):
        for tabledata in row.find_all('td'):
            searchvalue = request.POST['search_item'].get()
            if tabledata.text == searchvalue:
                data = tabledata.text
                request.session['data'] = data


def covid_symptoms(request):
    symptom = requests.get('https://www.who.int/health-topics/coronavirus#tab=tab_3')
    data = beauty(symptom.content, 'html.parser')
    # symp = data.findAll('div', class_="sf_colsOut tabContent")
    # for i in symp:
    #     symptoms = i.text
    #     [x.replace('\n', '') for x in symptoms]
    one = data.select('.tabContent li')
    # lines = symptoms.split('.')
    # for line in lines:
    #     symptoms1 = line
    #     print(line)



    # symptom = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    # data = urllib.request.urlopen(symptom).read()
    # symptom1 = data.decode('ISO-8859-1')
    # print(symptoms.headers['content-type'])

    c = {
        # 'symptoms': symptoms
        'one': one
    }
    c.update(csrf(request))
    return render(request, 'Tracker/symptoms.html', c)
    
    
@csrf_exempt
def health_history(request):
    data = request.session.get('data')
    disclaimer = 'NB: This questionnaire, and its results, does not in any way act as an alternative to the diagnosis results that would be available from tests done at an actual health institution. \n This is only meant to give predictions for probability of infection based on the input provided by the site users on their health and travel history, to advice them on how urgently they may need to visit a health center of their choice'

    c = {
        'disclaimer': disclaimer,
        'data': data
    }
    c.update(csrf(request))
    return render(request, 'Tracker/health.html', c)


def travel_history(request):
    travelstr = 'Enter details of your health history here'
    c = {
        'travelstr': travelstr
    }
    c.update(csrf(request))
    return render(request, 'Tracker/travel.html', c)


def feedback(request):
    statement = 'Here is how vulnerable you may be to covid 19 infection'
    c = {
        'statement': statement
    }
    return render(request, 'Tracker/infectionfeedback.html', c)


def contact(request):
    contact_info = 'The following is a list of free hotlines and toll numbers you can call whenever in any covid-19 health emergency'
    c = {
        'contact_info': contact_info
    }
    return render(request, 'Tracker/contact.html', c)
