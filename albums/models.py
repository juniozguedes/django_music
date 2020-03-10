from django.db import models
from artists.models import Artist

class Album(models.Model):
    album_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.album_name