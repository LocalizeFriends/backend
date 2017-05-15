from django.db import models


class UserLocation(models.Model):
    user_id = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=9, decimal_places=7)


class MeetupProposal(models.Model):
    organizer_id = models.IntegerField()
    creation_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    place_name = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=8, decimal_places=6)
    cancelled = models.BooleanField(default=False)

    def to_api_dict(self):
        return {
            'id': self.id,
            'organizer_id': self.organizer_id,
            'creation_timestamp_ms': int(self.creation_time.timestamp() * 1000),
            'name': self.name,
            'start_timestamp_ms': int(self.start_time.timestamp() * 1000),
            'place_name': self.place_name,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'cancelled': self.cancelled,
            'invitees': [
                {
                    'id': invitee.user_id,
                    'accepted': invitee.accepted
                }
                for invitee in self.invitee_set.all()
            ]
        }


class Invitee(models.Model):
    user_id = models.IntegerField(db_index=True)
    meetup_proposal = models.ForeignKey(MeetupProposal, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)


class UserCloudMessagingAddress(models.Model):
    user_id = models.IntegerField(db_index=True)
    address = models.CharField(max_length=255) # bigger than needed for now
    expiration_time = models.DateTimeField()
