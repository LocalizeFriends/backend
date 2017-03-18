from django import forms

class UpdateLocationForm(forms.Form):
    fbtoken = forms.CharField()
    lng = forms.FloatField(min_value=-180, max_value=180)
    lat = forms.FloatField(min_value=-90, max_value=90)
