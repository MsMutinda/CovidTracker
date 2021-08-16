from django import forms
from django.forms import ModelForm
from .models import Health, Travel


class HealthForm(forms.ModelForm):
    class Meta:
        model = Health
        fields = ['gender', 'age', 'disease', 'medication', 'transplant', 'vaccination']


class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['risk_areas', 'crowdy_places', 'international_travel', 'covidvictim_contact']
