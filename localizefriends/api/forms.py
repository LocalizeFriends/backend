from django import forms
from django.core.validators import validate_comma_separated_integer_list

class LocalizeFriendsApiForm(forms.Form):
    fbtoken = forms.CharField()


class UpdateLocationForm(LocalizeFriendsApiForm):
    lng = forms.DecimalField(min_value=-180, max_value=180, max_digits=9, decimal_places=6)
    lat = forms.DecimalField(min_value=-90, max_value=90, max_digits=8, decimal_places=6)


class GetFriendsLocationsForm(LocalizeFriendsApiForm):
    pass


class CreateMeetupProposalForm(LocalizeFriendsApiForm):
    name = forms.CharField(max_length=255)
    timestamp_ms = forms.IntegerField()
    place_name = forms.CharField(max_length=255)
    lng = forms.DecimalField(min_value=-180, max_value=180, max_digits=9, decimal_places=6)
    lat = forms.DecimalField(min_value=-90, max_value=90, max_digits=8, decimal_places=6)
    invite = forms.CharField(validators=[validate_comma_separated_integer_list])
