from django.urls import path

from . import views

urlpatterns = [
    path('all', views.getAlbums, name='getAlbums'), #Get all albums in database
    path('getid/<str:id>', views.getAlbumById, name='getAlbumById'), #Search album by id. It's a string cause if the Album_id doesn't exist on Deezer, it'll be alphanumeric on database to avoid conflict with the API
    path('getname/<str:name>', views.getAlbumByName, name='getAlbumByName'), #Search by Album name
    path('add/', views.addAlbum, name='addAlbum'), #Add new Album passing name
    path('update/', views.updateAlbum, name='updateAlbum'), #Update Album by Album_id
    path('delete/', views.deleteAlbum, name='deleteAlbum'), #Delete Album by Album_id
]