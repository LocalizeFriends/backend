from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist

import facebook

from .models import Location
from .forms import UpdateLocationForm, GetFriendsPositionsForm

from pprint import pprint

FB_APP_ID = 1908151672751269

def index(request):
    return HttpResponse('Hi, this is API.')

@require_POST
def update_location(request):
    form = UpdateLocationForm(request.POST)
    if form.is_valid():
        try:
            graph = facebook.GraphAPI(access_token=form.cleaned_data['fbtoken'], version='2.8')
            user = graph.get_object('me')
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

        location = Location(
            user_id = user['id'],
            longitude = form.cleaned_data['lng'],
            latitude = form.cleaned_data['lat'])
        location.save()

        return JsonResponse({
            'success': True
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'There were validation errors.',
            'errors': form.errors
        }, status=400)

@require_GET
def get_friends_positions(request):
    form = GetFriendsPositionsForm(request.GET)
    if form.is_valid():
        try:
            graph = facebook.GraphAPI(access_token=form.cleaned_data['fbtoken'], version='2.8')
            result = graph.get_object(id=FB_APP_ID, fields='context.fields(friends_using_app)')
            result = result['context']['friends_using_app']
            friends_using_app = []
            while True:
                friends_using_app.extend(result['data'])
                next_page = result['paging'].get('next')
                if not next_page:
                    break
                next_page_path = next_page.replace(facebook.FACEBOOK_GRAPH_URL, '')
                result = graph.request(next_page_path)
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

        for friend in friends_using_app:
            try:
                location = Location.objects.filter(user_id=friend['id']).latest('timestamp')
                friend['location'] = {
                    'timestamp_ms': int(location.timestamp.timestamp() * 1000),
                    'longitude': location.longitude,
                    'latitude':  location.latitude
                }
            except ObjectDoesNotExist:
                friend['location'] = None

        return JsonResponse({
            'success': True,
            'data': friends_using_app
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'There were validation errors.',
            'errors': form.errors
        }, status=400)
