from django import forms
from django.core.validators import validate_comma_separated_integer_list

class LocalizeFriendsApiForm(forms.Form):
    fbtoken = forms.CharField()


class CoordinatesApiForm(forms.Form):
    lng = forms.DecimalField(min_value=-180, max_value=180, max_digits=10, decimal_places=7)
    lat = forms.DecimalField(min_value=-90, max_value=90, max_digits=9, decimal_places=7)


class UpdateLocationForm(LocalizeFriendsApiForm, CoordinatesApiForm):
    pass


class GetFriendsLocationsForm(LocalizeFriendsApiForm):
    pass


class GetFriendsWithinRangeForm(LocalizeFriendsApiForm, CoordinatesApiForm):
    radius = forms.IntegerField(min_value=1)


class CreateMeetupProposalForm(LocalizeFriendsApiForm, CoordinatesApiForm):
    name = forms.CharField(max_length=255)
    timestamp_ms = forms.IntegerField()
    place_name = forms.CharField(max_length=255)
    invite = forms.CharField(validators=[validate_comma_separated_integer_list])


class SaveCloudMessagingAddressForm(LocalizeFriendsApiForm):
    address = forms.CharField(min_length=50, max_length=255)
    expiration_time_ms = forms.IntegerField()


class ChangeMeetupProposalStatusValueForm(LocalizeFriendsApiForm):
    value = forms.IntegerField(min_value=0, max_value=1)
