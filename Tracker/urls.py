from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.stats, name='stats'),
    path('symptoms/', views.covid_symptoms, name='symptoms'),
    path('health/', views.health_history, name='health_history'),
    path('travel/', views.travel_history, name='travel_history'),
    path('feedback/', views.feedback, name='feedback')
]
