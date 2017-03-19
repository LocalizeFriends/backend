from django.db import models


class UserLocation(models.Model):
    user_id = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)


class MeetupProposal(models.Model):
    organizer_id = models.IntegerField()
    creation_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    place_name = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    cancelled = models.BooleanField(default=False)


class Invitee(models.Model):
    user_id = models.IntegerField(db_index=True)
    meetup_proposal = models.ForeignKey(MeetupProposal, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
