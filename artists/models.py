from django.db import models


class Artist(models.Model):
    artist_id = models.CharField(max_length=50, unique=True) #Artistas não existentes no Deezer serão cadastrados com ID's Alfanuméricos para não colidir com a API de consulta.
    name = models.CharField(max_length=50, unique=True)
    link = models.URLField(max_length=100)
    tracklist = models.URLField(max_length=100)