from django.urls import path

from . import views

urlpatterns = [
    path('all', views.getArtists, name='getArtists'), #Get all artists in database
    path('getid/<str:id>', views.getArtistById, name='getArtistById'), #Search artist by id. It's a string cause if the artist_id doesn't exist on Deezer, it'll be alphanumeric on database to avoid conflict with the API
    path('getname/<str:name>', views.getArtistByName, name='getArtistByName'), #Search by artist name
    path('add/', views.addArtist, name='addArtist'), #Add new artist passing name
    path('update/', views.updateArtist, name='updateArtist'), #Update Artist by artist_id
    path('delete/', views.deleteArtist, name='deleteArtist'), #Delete Artist by artist_id
]