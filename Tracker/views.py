from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from Tracker.models import *
from Tracker.forms import *
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
import json
from bs4 import BeautifulSoup as beauty
import requests
from six.moves import urllib
import pandas as pd
from plotly.graph_objs import Bar, Layout, Figure, Scatter
# import plotly.express as px
from plotly.offline import plot
from django.template.loader import render_to_string
pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')


def homepage(request):
    resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)
    respdata1 = json.loads(resp)
    # Global stats visualization
    plotsdata = {
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
    # layout = Layout(barmode='group', title='Global Statistics')
    plot_div = plot([Bar(x=xdata, y=ydata, marker_color='orange')], output_type='div', show_link=False, link_text="")
    # plot_div.update_xaxes(rangemode="tozero")
    # dataplot = [{'type': 'bar', 'x': xdata, 'y': ydata}]
    # plotlayout = {'title': 'Global Statistics', 'xaxis': {'title': 'Case categories'},
    #               'yaxis': {'title': 'Number of cases'}}
    # fig = {'data': dataplot, 'layout': plotlayout}

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
        'plot_div': plot_div
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


def symptoms(request):
    symptom = requests.get('https://www.who.int/health-topics/coronavirus#tab=tab_3')
    data = beauty(symptom.content, 'html.parser')
    # symp = data.findAll('div', class_="sf_colsOut tabContent")
    # for i in symp:
    #     symptoms = i.text
    #     [x.replace('\n', '') for x in symptoms]
    one = data.select('.tabContent li')
    c = {
        # 'symptoms': symptoms
        'one': one
    }
    c.update(csrf(request))
    return render(request, 'Tracker/symptoms.html', c)
    
    
def health(request):
    disclaimer = 'NB: This questionnaire, and its results, does not in any way act as an alternative to the diagnosis results that would be available from tests done at an actual health institution. \n This is only meant to give predictions for probability of infection based on the input provided by the site users on their health and travel history, to advice them on how urgently they may need to visit a health center of their choice'
    c = {
        # 'form': HealthForm(),
        'disclaimer': disclaimer
    }
    c.update(csrf(request))
    return render(request, 'Tracker/health.html', c)


def save_health(request):
    if request.POST:
        form = HealthForm(request.POST)
        if form.is_valid():
            # form.save()
            query = {
                'gender': form.cleaned_data.get('gender'),
                'age': form.cleaned_data.get('age'),
                'diseases': request.POST.getlist('diseases'),
                'medication': form.cleaned_data.get('medication'),
                'transplant': form.cleaned_data.get('transplant'),
                'vaccination': form.cleaned_data.get('vaccination'),
            }
            Health.objects.create(**query)
            return render(request, 'Tracker/travel.html')


def travel(request):
    disclaimer = 'NB: This questionnaire, and its results, does not in any way act as an alternative to the diagnosis results that would be available from tests done at an actual health institution. \n This is only meant to give predictions for probability of infection based on the input provided by the site users on their health and travel history, to advice them on how urgently they may need to visit a health center of their choice'
    c = {
        'disclaimer': disclaimer
    }
    c.update(csrf(request))
    return render(request, 'Tracker/travel.html', c)


def save_travel(request):
    if request.method == 'POST':
        form = TravelForm(request.POST)
        if form.is_valid():
            query = {
                "risk_areas": form.cleaned_data.get("risk_areas"),
                "crowdy_places": form.cleaned_data.get("crowdy_places"),
                "international_travel": form.cleaned_data.get("international_travel"),
                "victim_contact": form.cleaned_data.get("victim_contact"),
            }
            Travel.objects.create(**query)
        return render(request, 'Tracker/infectionfeedback.html')

        # return HttpResponseRedirect(reverse('Tracker:feedback'))


def feedback(request):
    statement = 'Here is how vulnerable you may be to covid 19 infection'
    c = {
        'statement': statement
    }
    return render(request, 'Tracker/infectionfeedback.html', c)


def contact(request):

    return render(request, 'Tracker/contact.html')
