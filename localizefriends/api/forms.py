from django import forms


class LocalizeFriendsApiForm(forms.Form):
    fbtoken = forms.CharField()


class UpdateLocationForm(LocalizeFriendsApiForm):
    lng = forms.FloatField(min_value=-180, max_value=180)
    lat = forms.FloatField(min_value=-90, max_value=90)


class GetFriendsPositionsForm(LocalizeFriendsApiForm):
    pass
