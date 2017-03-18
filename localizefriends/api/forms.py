from django import forms


class LocalizeFriendsApiForm(forms.Form):
    fbtoken = forms.CharField()


class UpdateLocationForm(LocalizeFriendsApiForm):
    lng = forms.DecimalField(min_value=-180, max_value=180, max_digits=9, decimal_places=6)
    lat = forms.DecimalField(min_value=-90, max_value=90, max_digits=8, decimal_places=6)


class GetFriendsLocationsForm(LocalizeFriendsApiForm):
    pass
