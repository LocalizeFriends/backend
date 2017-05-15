from django.conf.urls import url

from . import views

app_name = 'urls'
urlpatterns = [
    url(r'^location$', views.update_location, name='update_location'),
    url(r'^friends_locations$', views.get_friends_locations, name='get_friends_locations'),
    url(r'^meetup_proposal$', views.create_meetup_proposal, name='create_meetup_proposal'),
    url(r'^meetup_proposal/(?P<meetup_id>[0-9]+)/accept$', views.accept_meetup_proposal, name='accept_meetup_proposal'),
    url(r'^meetup_proposal/(?P<meetup_id>[0-9]+)/cancel$', views.cancel_meetup_proposal, name='cancel_meetup_proposal'),
    url(r'^meetup_proposal/(?P<meetup_id>[0-9]+)$', views.get_meetup_proposal, name='get_meetup_proposal'),
    url(r'^meetup_proposals$', views.get_meetup_proposals, name='get_meetup_proposals'),
    url(r'^friends_within_range$', views.get_friends_within_range, name='get_friends_within_range'),
    url(r'^cloud_messaging_address$', views.save_cloud_messaging_address, name='save_cloud_messaging_address'),
    url(r'^$', views.index, name='index'),
]
