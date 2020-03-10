import json
import random
import string
import requests
from .models import Album
from artists.models import Artist
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def getAlbums(request):
    albums = Album.objects.all()
    data = {"results": list(albums.values("name", "album_id", "artist__name", "artist__artist_id"))}
    return JsonResponse(data)
    
def getAlbumByName(request, name):
    try: 
        Album.objects.get(name__icontains=name)
        albums = Album.objects.filter(name__icontains=name)
        data = {"results": list(albums.values("name", "album_id", "artist__name", "artist__artist_id"))}
        return JsonResponse(data)
    except ObjectDoesNotExist:
        response = requests.get('https://api.deezer.com/search/album?q=%s' %name)
        albums_data = response.json()
        if albums_data.get('total') == 0:
            return HttpResponse('No album according to URL param Name')
        else:
            album_artist = Artist.objects.filter(artist_id=albums_data['data'][0]['artist']['id'])
            if album_artist:
                album = Album(name=albums_data['data'][0]['title'], album_id=albums_data['data'][0]['id'],artist=album_artist.get())
                album.save()
                return redirect('getAlbumByName', name=album.name)
            else: #Caso não exista o artist na nossa base, varre a API e cadastra o artista para instanciar o album
                artist_response = requests.get('https://api.deezer.com/artist/%s' %albums_data['data'][0]['artist']['id'])
                artists_data = artist_response.json()
                artist = Artist(name=artists_data['name'], artist_id=artists_data['id'],link=artists_data['link'],tracklist=artists_data['tracklist'])
                artist.save()
                return redirect('getAlbumByName', name=name)

def getAlbumById(request, id):
    try: 
        Album.objects.get(album_id=id)
        albums = Album.objects.filter(album_id=id)
        data = {"results": list(albums.values("name", "album_id", "artist__name", "artist__artist_id"))}
        return JsonResponse(data)
    except ObjectDoesNotExist:
        response = requests.get('https://api.deezer.com/album/%s' %id)
        albums_data = response.json()
        if albums_data.get('error'):
            return HttpResponse('No album according to URL param ID')
        else:
            album_artist = Artist.objects.filter(artist_id=albums_data['contributors'][0]['id'])
            if album_artist:
                album = Album(name=albums_data['title'], album_id=albums_data['id'],artist=album_artist.get())
                album.save()
                return redirect('getAlbumById', id=album.album_id)
            else: #Caso não exista o artist na nossa base, varre a API e cadastra o artista para instanciar o album
                artist_response = requests.get('https://api.deezer.com/artist/%s' %albums_data['contributors'][0]['id'])
                artists_data = artist_response.json()
                artist = Artist(name=artists_data['name'], artist_id=artists_data['id'],link=artists_data['link'],tracklist=artists_data['tracklist'])
                artist.save()
                return redirect('getAlbumById', id=album.album_id)

def addAlbum(request):
    N = 27
    pi = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    if request.GET.get('name'):
        try:
            Album.objects.get(name__icontains=request.GET.get('name'))
            albums = Album.objects.filter(name__icontains=request.GET.get('name'))
            data = {"results": list(albums.values("name", "artist__name", "artist__artist_id"))}
            return JsonResponse(data)
        except ObjectDoesNotExist:
            if request.GET.get('artist_id'):
                album_list_response = requests.get('https://api.deezer.com/artist/%s/albums' %request.GET.get('artist_id'))
                album_data = album_list_response.json()
                album_list = []
                x = 0
                while x < (len(album_data['data'])):
                    album_title = album_data['data'][x]['title']
                    album_list.append(album_title)
                    x+=1
                if request.GET.get('name') in album_list:
                    #album = Album(name=request.GET.get('name'), album_id=getapiequaltoartistalbum, artist=artistid)
                    #album.save()
                    return redirect('getAlbumByName', name=request.GET.get('name'))
                else:
                    quit()
            else:
                return HttpResponse('The artist_id param is required to associate album to artist')
    else:
        return HttpResponse('The {{name}} param and the {{artist_id}} param is required to associate album to artist')

def updateAlbum(request):
    try:
        Album.objects.get(album_id=request.GET.get('album_id'))
        album = Album.objects.get(album_id=request.GET.get('album_id'))
        album.name = request.GET.get('name')
        album.save()
        return redirect('getAlbumByName', name=album.name)
    except ObjectDoesNotExist:
        return HttpResponse('artist_id was not found in the database, please check the correct id')

def deleteAlbum(request):
    try:
        Album.objects.get(album_id=request.GET.get('album_id'))
        album = Album.objects.get(album_id=request.GET.get('album_id'))
        album.delete()
        return HttpResponse('Album Deleted')
    except ObjectDoesNotExist:
        return HttpResponse('album_id was not found in the database, please check the correct id')