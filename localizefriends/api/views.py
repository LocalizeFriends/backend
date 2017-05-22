from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import UserLocation, MeetupProposal, Invitee, UserCloudMessagingAddress
from .forms import *
from .view_decorators import validate_with_form
from . import message_queue_client

import facebook
import pytz
import json
from pprint import pprint
from datetime import datetime
from geodesy import wgs84

FB_APP_ID = 1908151672751269

def index(request):
    return JsonResponse({
        'success': True,
        'message': 'Hi, this is API.'
    })

@require_POST
@validate_with_form(UpdateLocationForm)
def update_location(request, cleaned_data):
    if 'as_user_id' in request.POST:
        user = { 'id': request.POST['as_user_id'] }
    else:
        try:
            graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
            user = graph.get_object('me')
        except facebook.GraphAPIError as e:
            return JsonResponse({
                'success': False,
                'message': e.message
            }, status=403)

    location = UserLocation(
        user_id = user['id'],
        longitude = cleaned_data['lng'],
        latitude = cleaned_data['lat'])
    location.save()

    return JsonResponse({
        'success': True
    })

@require_GET
@validate_with_form(GetFriendsLocationsForm)
def get_friends_locations(request, cleaned_data):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
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

@require_GET
@validate_with_form(GetFriendsWithinRangeForm)
def get_friends_within_range(request, cleaned_data):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
        friends_using_app = fetch_friends_using_app(graph)
    except facebook.GraphAPIError as e:
        return JsonResponse({
            'success': False,
            'message': e.message
        }, status=403)

    friends_within_range = []

    for friend in friends_using_app:
        try:
            location = UserLocation.objects.filter(user_id=friend['id']).latest('timestamp')
            friend_lng = location.longitude
            friend_lat = location.latitude
            friend_dist = wgs84.distance((cleaned_data['lat'], cleaned_data['lng']),
                                         (friend_lat, friend_lng))
            print(friend_dist)
            if friend_dist < cleaned_data['radius']:
                friend['distance'] = friend_dist
                friend['location'] = {
                    'timestamp_ms': int(location.timestamp.timestamp() * 1000),
                    'longitude': friend_lng,
                    'latitude':  friend_lat
                }
                friends_within_range.append(friend)
        except ObjectDoesNotExist:
            pass

    return JsonResponse({
        'success': True,
        'data': friends_within_range
    })

@require_POST
@validate_with_form(CreateMeetupProposalForm)
def create_meetup_proposal(request, cleaned_data):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
        user = graph.get_object('me')
        friends_using_app = fetch_friends_using_app(graph)
    except facebook.GraphAPIError as e:
        return JsonResponse({
            'success': False,
            'message': e.message
        }, status=403)

    friends_using_app_ids = list(map(lambda f: f['id'], friends_using_app))
    invitees_ids = [ int(user_id) for user_id in set(cleaned_data['invite'].split(',')) ]
    for invitee_id in invitees_ids:
        if invitee_id not in friends_using_app_ids:
            return JsonResponse({
                'success': False,
                'message': 'User with id {} is not a friend using app.'.format(invitee_id)
            }, status=403)

    meetup_proposal = MeetupProposal(
        organizer_id = user['id'],
        name = cleaned_data['name'],
        start_time = datetime.fromtimestamp(cleaned_data['timestamp_ms'] / 1000, pytz.utc),
        place_name = cleaned_data['place_name'],
        longitude = cleaned_data['lng'],
        latitude = cleaned_data['lat'])
    meetup_proposal.save()

    for invitee_id in invitees_ids:
        invitee = Invitee(
            user_id=invitee_id,
            meetup_proposal=meetup_proposal)
        invitee.save()

    send_fcm_message(invitees_ids, {
        'type': 'meetup_proposal_invitation_received',
        'meetup_id': int(meetup_proposal.id),
        'organizer_id': user['id']
    })

    return JsonResponse({
        'success': True
    })

@require_POST
@validate_with_form(ChangeMeetupProposalStatusValueForm)
def accept_meetup_proposal(request, cleaned_data, meetup_id):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
        user = graph.get_object('me')
        friends_using_app = fetch_friends_using_app(graph)
    except facebook.GraphAPIError as e:
        return JsonResponse({
            'success': False,
            'message': e.message
        }, status=403)

    try:
        invitee = Invitee.objects.get(
            Q(user_id=user['id']),
            Q(meetup_proposal__id=meetup_id)
        )
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Meetup proposal was not found or the status cannot be changed by the current user.'
        }, status=404)

    invitee.accepted = bool(cleaned_data['value'])
    invitee.save()
    recipients_ids = [ user['user_id'] for user
                       in Invitee.objects.filter(
                           ~Q(user_id=user['id']),
                           Q(meetup_proposal__id=meetup_id)
                       ).values('user_id') ]
    recipients_ids.append(MeetupProposal.objects.get(pk=meetup_id).organizer_id)
    send_fcm_message(recipients_ids, {
        'type': 'meetup_proposal_invitation_change',
        'meetup_id': int(meetup_id),
        'user_id': user['id'],
        'new_status': invitee.accepted
    })

    return JsonResponse({
        'success': True
    })

@require_POST
@validate_with_form(ChangeMeetupProposalStatusValueForm)
def cancel_meetup_proposal(request, cleaned_data, meetup_id):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
        user = graph.get_object('me')
        friends_using_app = fetch_friends_using_app(graph)
    except facebook.GraphAPIError as e:
        return JsonResponse({
            'success': False,
            'message': e.message
        }, status=403)

    try:
        meetup_proposal = MeetupProposal.objects.get(
            Q(id=meetup_id),
            Q(organizer_id=user['id'])
        )
        meetup_proposal.cancelled = bool(cleaned_data['value'])
        meetup_proposal.save()
        recipients_ids = [ user['user_id'] for user
                         in meetup_proposal.invitee_set.values('user_id') ]
        send_fcm_message(recipients_ids, {
            'type': 'meetup_proposal_cancel_change',
            'meetup_id': int(meetup_id),
            'user_id': user['id'],
            'new_status': meetup_proposal.cancelled
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Meetup proposal was not found or the status cannot be changed by the current user.'
        }, status=404)

    return JsonResponse({
        'success': True
    })

@require_GET
@validate_with_form(LocalizeFriendsApiForm)
def get_meetup_proposal(request, cleaned_data, meetup_id):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
        user = graph.get_object('me')
    except facebook.GraphAPIError as e:
        return JsonResponse({
            'success': False,
            'message': e.message
        }, status=403)

    try:
        meetup = MeetupProposal.objects.get(
            Q(organizer_id=user['id']) | Q(invitee__user_id=user['id']),
            pk=meetup_id
        )
    except ObjectDoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Meetup proposal was not found or cannot be accessed by the current user.'
        }, status=404)

    return JsonResponse({
        'success': True,
        'data': meetup.to_api_dict()
    })

@require_GET
@validate_with_form(LocalizeFriendsApiForm)
def get_meetup_proposals(request, cleaned_data):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
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

@require_POST
@validate_with_form(SaveCloudMessagingAddressForm)
def save_cloud_messaging_address(request, cleaned_data):
    try:
        graph = facebook.GraphAPI(access_token=cleaned_data['fbtoken'], version='2.8')
        user = graph.get_object('me')
    except facebook.GraphAPIError as e:
        return JsonResponse({
            'success': False,
            'message': e.message
        }, status=403)

    user_address = UserCloudMessagingAddress(
        user_id = user['id'],
        address = cleaned_data['address'],
        expiration_time = datetime.fromtimestamp(cleaned_data['expiration_time_ms'] / 1000, pytz.utc))
    user_address.save()

    return JsonResponse({
        'success': True
    })

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

def send_fcm_message(user_ids, msg):
    print(user_ids)
    receiver_addrs = []
    for user_id in user_ids:
        receiver = UserCloudMessagingAddress.objects.filter(
            Q(user_id=user_id),
            Q(expiration_time__gt=datetime.now(tz=pytz.utc))
        ).order_by('-expiration_time').first()
        print(receiver)
        if receiver:
            print(receiver.address)
            receiver_addrs.append(receiver.address)
    if len(receiver_addrs) > 0:
        message_queue_client.send_fcm_message(receiver_addrs, msg)
