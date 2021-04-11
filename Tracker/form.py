from django import forms

class healthForm(forms.Form):
    health_history = forms.CharField(label='yourdata', maxlength=100)