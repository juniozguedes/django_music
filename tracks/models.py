from django.db import models
from albums.models import Album

class Track(models.Model):
    track_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150, null=False, blank=False, unique=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.track_name