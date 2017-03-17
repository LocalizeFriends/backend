from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django import forms

import facebook

from .models import Location


def index(request):
    return HttpResponse('Hi, this is API.')

@require_POST
def update_location(request):

    class LocationForm(forms.Form):
        fbtoken = forms.CharField()
        lng = forms.FloatField(min_value=-180, max_value=180)
        lat = forms.FloatField(min_value=-90, max_value=90)

    location_form = LocationForm(request.POST)
    if location_form.is_valid():
        try:
            graph = facebook.GraphAPI(access_token=location_form.cleaned_data['fbtoken'], version='2.8')
            user = graph.get_object('me')
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

        location = Location(
            user_id = user['id'],
            longitude = location_form.cleaned_data['lng'],
            latitude = location_form.cleaned_data['lat'])
        location.save()

        return JsonResponse({
            'success': True
        })
    return JsonResponse({
        'success': False,
        'message': 'There were validation errors.',
        'errors': location_form.errors
    }, status=400)
