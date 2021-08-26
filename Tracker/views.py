from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from Tracker.models import *
from Tracker.forms import *
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as beauty
import requests
# from six.moves import urllib
import pandas as pd
import matplotlib
# from future.moves import tkinter as tk
# try:
#     import Tkinter as tk # this is for python2
# except:
#     import tkinter as tk
# matplotlib.use('TkAgg')
from matplotlib.pyplot import *
import numpy as np
from plotly.graph_objs import Bar, Layout, Figure, Scatter
from plotly.offline import plot
from django.template.loader import render_to_string
pd.set_option('display.width', 1000)
pd.set_option('colheader_justify', 'center')


def homepage(request):
    resp = json.dumps(requests.get('https://api.covid19api.com/summary').json(), sort_keys=True, indent=4)
    respdata1 = json.loads(resp)
    request.session['respdata1'] = respdata1

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
    plot_div = plot([Bar(x=xdata, y=ydata, marker_color='orange')], output_type='div', show_link=False, link_text="")

    # Data per country
    for item in respdata1.keys():
        if item == 'Countries':
            respdata = respdata1[item]
            df_old = pd.DataFrame(respdata)
            df = df_old.drop(columns=["Premium", "Slug", "ID"])
            # df_obj1 = list(df.to_html(classes='mystyle', index=False))
            df_obj = df.to_html(classes='mystyle', index=False)
            # paginated = Paginator(df_obj1, 14)
            # page_number = request.GET.get('page')
            # df_obj = paginated.get_page(page_number)
            request.session['df_obj'] = df_obj

    c = {
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


@login_required
def save_health(request):
    if request.POST:
        form = HealthForm(request.POST)
        if form.is_valid():
            user2 = User.objects.values_list("is_active").filter(id=request.user.id)
            query = {
                'is_active': user2,
                'gender': form.cleaned_data.get('gender'),
                'age': form.cleaned_data.get('age'),
                'diseases': request.POST.getlist('diseases'),
                'medication': form.cleaned_data.get('medication'),
                'transplant': form.cleaned_data.get('transplant'),
                'vaccination': form.cleaned_data.get('vaccination'),
            }
            Health.objects.create(**query)
            return render(request, 'Tracker/travel.html')

        return render(request, 'Tracker/travel.html')


def travel(request):
    disclaimer = 'NB: This questionnaire, and its results, does not in any way act as an alternative to the diagnosis results that would be available from tests done at an actual health institution. \n This is only meant to give predictions for probability of infection based on the input provided by the site users on their health and travel history, to advice them on how urgently they may need to visit a health center of their choice'
    c = {
        'disclaimer': disclaimer
    }
    c.update(csrf(request))
    return render(request, 'Tracker/travel.html', c)


@login_required
def save_travel(request):
    if request.method == 'POST':
        form = TravelForm(request.POST)
        if form.is_valid():
            user2 = User.objects.values_list("is_active").filter(id=request.user.id)
            query = {
                'is_active': user2,
                "risk_areas": form.cleaned_data.get("risk_areas"),
                "crowdy_places": form.cleaned_data.get("crowdy_places"),
                "international_travel": form.cleaned_data.get("international_travel"),
                "victim_contact": form.cleaned_data.get("victim_contact"),
            }
            Travel.objects.create(**query)
        return render(request, 'Tracker/infectionfeedback.html')
        # return HttpResponseRedirect(reverse('Tracker:feedback'))



def health_travel_analysis(request):
    # age 18-25
    health1 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and diseases is not NULL")
    health2 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and medication like 'yes%%'")
    health3 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and transplant like 'yes%%'")
    health4 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and vaccination like 'no%%'")
    health_results1 = len(list(chain(health1, health2, health3, health4))) + 1

    # age 26-35
    health5 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and diseases is not NULL")
    health6 = Health.objects.raw("select * from health where is_active = true and age like '26-35%%' and medication like 'yes%%'")
    health7 = Health.objects.raw("select * from health where is_active = true and age like '26-35%%' and transplant like 'yes%%'")
    health8 = Health.objects.raw("select * from health where is_active = true and age like '25-35%%' and vaccination like 'no%%'")
    health_results2 = len(list(chain(health5, health6, health7, health8))) + 2

    # age 36-54
    health9 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and diseases is not NULL")
    health10 = Health.objects.raw("select * from health where is_active = true and age like '36-54%%' and medication like 'yes%%'")
    health11 = Health.objects.raw("select * from health where is_active = true and age like '36-54%%' and transplant like 'yes%%'")
    health12 = Health.objects.raw("select * from health where is_active = true and age like '36-54%%' and vaccination like 'no%%'")
    health_results3 = len(list(chain(health9, health10, health11, health12))) + 3

    # age 55-74
    health13 = Health.objects.raw("select * from health where is_active = true and age like '18-25%%' and diseases is not NULL")
    health14 = Health.objects.raw("select * from health where is_active = true and age like '55-74%%' and medication like 'yes%%'")
    health15 = Health.objects.raw("select * from health where is_active = true and age like '55-74%%' and transplant like 'yes%%'")
    health16 = Health.objects.raw("select * from health where is_active = true and age like '55-74%%' and vaccination like 'no%%'")
    health_results4 = len(list(chain(health13, health14, health15, health16))) + 4

    # age 75 and above
    health17 = Health.objects.raw("select * from health where is_active = true and age like '75 and above%%' and diseases is not NULL")
    health18 = Health.objects.raw("select * from health where is_active = true and age like '75 and above%%' and medication like 'yes%%'")
    health19 = Health.objects.raw("select * from health where is_active = true and age like '75 and above%%' and transplant like 'yes%%'")
    health20 = Health.objects.raw("select * from health where is_active = true and age like '75 and above%%' and vaccination like 'no%%'")
    health_results5 = len(list(chain(health17, health18, health19, health20))) + 5

    # travel data retrieval
    # travel_results = Travel.objects.raw("select * from travel where (risk_areas, crowdy_places, international_travel, victim_contact) LIKE 'Yes%%'")
    travel1 = Travel.objects.raw("select * from travel where is_active = true and risk_areas like 'Yes%%'")
    travel2 = Travel.objects.raw("select * from travel where is_active = true and crowdy_places like 'Yes%%'")
    travel3 = Travel.objects.raw("select * from travel where is_active = true and international_travel like 'Yes%%'")
    travel4 = Travel.objects.raw("select * from travel where is_active = true and victim_contact like 'Yes%%'")
    travel_results = len(list(chain(travel1, travel2, travel3, travel4)))

    # health + travel analysis

    # change above health and travel results to use actual logged in user id and not defined user id

    age = Health.objects.values('age').filter(user_id = request.user.id)
    all = User.objects.all().filter(is_superuser = False, is_active = True)
    print(all)

    print(age)
    # person_age = Health.objects.values('age').filter(is_active = True)

    # for age in person_age:
    if age == '75 and above' and travel_results >= 4:
        risk = health_results5 + travel_results
        message = 'Risk of infection: LOW'
        message2 = 'Probability of getting seriously ill: VERY HIGH'
    elif age == '55-74' and travel_results == 3:
        risk = health_results4 + travel_results
        message = 'Risk of infection: LOW'
        message2 = 'Probability of getting seriously ill: HIGH'
    elif age == '36-54' and len(travel_results) == 2:
        risk = health_results3 + travel_results
        message = 'Risk of infection: MEDIUM'
        message2 = 'Probability of getting seriously ill: MEDIUM'
    elif age == '26-35' and len(travel_results) == 2:
        risk = health_results2 + travel_results
        message = 'Risk of infection: HIGH'
        message2 = 'Probability of getting seriously ill: MEDIUM'
    # age == '18-25' and len(travel_results) == 1
    risk = health_results1 + travel_results
    message = 'Risk of infection: VERY HIGH'
    message2 = 'Probability of getting seriously ill: LOW'

    c = {
        'risk': risk,
        'message': message,
        'message2': message2,
    }
    return render(request, 'Tracker/infectionfeedback.html', c)


def visualize_feedback(request):
    # graph to visualize risk factors
    age = ['75 and above', '55-74', '36-64', '26-35', '18-25']
    infection = ['LOW', 'MEDIUM', 'HIGH', 'VERY HIGH', 'paddingdata']
    illness = ['LOW', 'MEDIUM', 'HIGH', 'VERY HIGH', 'paddingdata']
    fig, ax = matplotlib.pyplot.subplots()
    ax.plot(age, infection, label="Risk of infection", color='orange')
    ax.plot(age, illness, label="Probability of getting seriously ill", color='blue')
    ax.legend()
    plt.show()
    for k, v in data.items():
        plt.plot(range(1, len(v) + 1), v, '.-', label=k)

    c = {

    }
    return render(request, 'Tracker/infectionfeedback.html', c)

def feedback(request):
    statement = 'Here is how vulnerable you may be to covid 19 infection'
    c = {
        'statement': statement
    }
    return render(request, 'Tracker/infectionfeedback.html', c)


def contact(request):

    return render(request, 'Tracker/contact.html')
