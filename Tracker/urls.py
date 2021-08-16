from django.urls import path, include
from Tracker import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Tracker'
urlpatterns = [
    path('', views.homepage, name='home'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('health/', views.health, name='health'),
    path('health/save', views.save_health, name='save_health'),
    path('travel/', views.travel, name='travel'),
    path('travel/save', views.save_travel, name='save_travel'),
    path('feedback/', views.feedback, name='feedback'),
    path('contacts/', views.contact, name='contact')
]
