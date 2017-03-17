from django.db import models


class Location(models.Model):
    user_id = models.IntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=3)
    latitude = models.DecimalField(max_digits=8, decimal_places=3)
