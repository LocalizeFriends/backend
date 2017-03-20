from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

import facebook

from .models import UserLocation, MeetupProposal, Invitee
from .forms import *

from pprint import pprint
from datetime import datetime
import pytz

FB_APP_ID = 1908151672751269

def index(request):
    return JsonResponse({
        'success': True,
        'message': 'Hi, this is API.'
    })

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

        location = UserLocation(
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
def get_friends_locations(request):
    form = GetFriendsLocationsForm(request.GET)
    if form.is_valid():
        try:
            graph = facebook.GraphAPI(access_token=form.cleaned_data['fbtoken'], version='2.8')
            friends_using_app = fetch_friends_using_app(graph)
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

        for friend in friends_using_app:
            try:
                location = UserLocation.objects.filter(user_id=friend['id']).latest('timestamp')
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

@require_POST
def create_meetup_proposal(request):
    form = CreateMeetupProposalForm(request.POST)
    if form.is_valid():
        try:
            graph = facebook.GraphAPI(access_token=form.cleaned_data['fbtoken'], version='2.8')
            user = graph.get_object('me')
            friends_using_app = fetch_friends_using_app(graph)
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

        friends_using_app_ids = list(map(lambda f: f['id'], friends_using_app))
        invitees_ids = set(form.cleaned_data['invite'].split(','))
        for invitee_id in invitees_ids:
            if invitee_id not in friends_using_app_ids:
                return JsonResponse({
                    'success': False,
                    'message': 'User with id {} is not a friend using app.'.format(invitee_id)
                }, status=403)

        meetup_proposal = MeetupProposal(
            organizer_id = user['id'],
            name = form.cleaned_data['name'],
            start_time = datetime.fromtimestamp(form.cleaned_data['timestamp_ms'] / 1000, pytz.utc),
            place_name = form.cleaned_data['place_name'],
            longitude = form.cleaned_data['lng'],
            latitude = form.cleaned_data['lat'])
        meetup_proposal.save()

        for invitee_id in invitees_ids:
            invitee = Invitee(
                user_id=invitee_id,
                meetup_proposal=meetup_proposal)
            invitee.save()

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
def get_meetup_proposals(request):
    form = LocalizeFriendsApiForm(request.GET)
    if form.is_valid():
        try:
            graph = facebook.GraphAPI(access_token=form.cleaned_data['fbtoken'], version='2.8')
            user = graph.get_object('me')
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

        meetups = MeetupProposal.objects.filter(
            Q(organizer_id=user['id']) | Q(invitee__user_id=user['id'])
        ).order_by('-start_time')

        return JsonResponse({
            'success': True,
            'data': [ meetup.to_api_dict() for meetup in meetups ]
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'There were validation errors.',
            'errors': form.errors
        }, status=400)

# --- views end ---

# helpers:

def fetch_friends_using_app(graph):
    result = graph.get_object(id=FB_APP_ID, fields='context.fields(friends_using_app)')
    result = result['context']['friends_using_app']
    friends_using_app = []
    while True:
        for friend in result['data']:
            friend['id'] = int(friend['id'])
        friends_using_app.extend(result['data'])
        next_page = result['paging'].get('next')
        if not next_page:
            break
        next_page_path = next_page.replace(facebook.FACEBOOK_GRAPH_URL, '')
        result = graph.request(next_page_path)
    return friends_using_app
