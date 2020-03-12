from django.urls import path

from . import views

urlpatterns = [
    path('all', views.getTracks, name='getTracks'), #Get all tracks in database
    path('getid/<str:id>', views.getTrackById, name='getTrackById'), #Search track by id. It's a string cause if the track_id doesn't exist on Deezer, it'll be alphanumeric on database to avoid conflict with the API
    path('getname/<str:name>', views.getTrackByName, name='getTrackByName'), #Search by Track name
    path('add/', views.addTrack, name='addTrack'), #Add new Track passing name & album_id
    path('update/', views.updateTrack, name='updateTrack'), #Update Track by Track id
    path('delete/', views.deleteTrack, name='deleteTrack'), #Delete Track by Track id
]