import json
import random
import string
import requests
from .models import Track
from albums.models import Album
from artists.models import Artist
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def getTracks(request):
    tracks = Track.objects.all()
    data = {"results": list(tracks.values("name", "track_id", "album__name", "album__album_id"))}
    return JsonResponse(data)
    
def getTrackByName(request, name):
    try: 
        Track.objects.get(name=name)
        tracks = Track.objects.filter(name__icontains=name)
        data = {"results": list(tracks.values("name", "track_id", "album__album_id"))}
        return JsonResponse(data)
    except ObjectDoesNotExist:
        response = requests.get('https://api.deezer.com/search/track?q=%s' %name)
        tracks_data = response.json()
        if tracks_data.get('total') == 0:
            return HttpResponse('No track according to URL param Name')
        else:
            album_artist = Artist.objects.filter(artist_id=tracks_data['data'][0]['artist']['id'])
            track_album = Album.objects.filter(album_id=tracks_data['data'][0]['album']['id'])
            if album_artist and track_album:
                track = Track(name=tracks_data['data'][0]['title'], track_id=tracks_data['data'][0]['id'],album=track_album.get())
                track.save()
                return redirect('getTrackByName', name=tracks_data['data'][0]['title'])
            elif album_artist and not track_album:
                album_response = requests.get('https://api.deezer.com/album/%s' %tracks_data['data'][0]['album']['id'])
                albums_data = album_response.json()
                album = Album(name=albums_data['title'], album_id=albums_data['id'], artist= album_artist.get())
                album.save()
                track = Track(name=tracks_data['data'][0]['title'], track_id=tracks_data['data'][0]['id'],album=album)
                track.save()
                return redirect('getTrackByName', name=tracks_data['data'][0]['title'])
            else:
                artist_response = requests.get('https://api.deezer.com/artist/%s' %tracks_data['data'][0]['artist']['id'])
                artists_data = artist_response.json()
                artist = Artist(name=artists_data['name'], artist_id=artists_data['id'],link=artists_data['link'],tracklist=artists_data['tracklist'])
                artist.save()
                album_response = requests.get('https://api.deezer.com/album/%s' %tracks_data['data'][0]['album']['id'])
                albums_data = album_response.json()
                album = Album(name=albums_data['title'], album_id=albums_data['id'], artist= artist)
                album.save()
                track = Track(name=tracks_data['data'][0]['title'], track_id=tracks_data['data'][0]['id'],album=album)
                track.save()
                return redirect('getTrackByName', name=tracks_data['data'][0]['title'])

def getTrackById(request, id):
    try: 
        Track.objects.get(track_id=id)
        tracks = Track.objects.filter(track_id=id)
        data = {"results": list(tracks.values("name", "track_id", "album__album_id"))}
        return JsonResponse(data)
    except ObjectDoesNotExist:
        response = requests.get('https://api.deezer.com/track/%s' %id)
        tracks_data = response.json()
        if tracks_data.get('error'):
            return HttpResponse('No track according to URL param ID')
        else:
            album_artist = Artist.objects.filter(artist_id=tracks_data['artist']['id'])
            track_album = Album.objects.filter(album_id=tracks_data['album']['id'])
            if album_artist and track_album:
                track = Track(name=tracks_data['title'], track_id=tracks_data['data']['id'],album=track_album.get())
                track.save()
                return redirect('getTrackByName', name=tracks_data['data']['title'])
            elif album_artist and not track_album:
                album_response = requests.get('https://api.deezer.com/album/%s' %tracks_data['data'][0]['album']['id'])
                albums_data = album_response.json()
                album = Album(name=albums_data['title'], album_id=albums_data['id'], artist= album_artist.get())
                album.save()
                track = Track(name=tracks_data['title'], track_id=tracks_data['id'],album=album)
                track.save()
                return redirect('getTrackByName', name=tracks_data['title'])
            else:
                artist_response = requests.get('https://api.deezer.com/artist/%s' %tracks_data['artist']['id'])
                artists_data = artist_response.json()
                artist = Artist(name=artists_data['name'], artist_id=artists_data['id'],link=artists_data['link'],tracklist=artists_data['tracklist'])
                artist.save()
                album_response = requests.get('https://api.deezer.com/album/%s' %tracks_data['album']['id'])
                albums_data = album_response.json()
                album = Album(name=albums_data['title'], album_id=albums_data['id'], artist= artist)
                album.save()
                track = Track(name=tracks_data['title'], track_id=tracks_data['id'],album=album)
                track.save()
                return redirect('getTrackByName', name=tracks_data['title'])

def addTrack(request):
    N = 27
    pi = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    if request.GET.get('name') and request.GET.get('album_id'):
        try:
            album = Album.objects.get(album_id=request.GET.get('album_id'))
            if album:
                tracks = album.track_set.all()
                track_list = []
                x = 0
                while x < (len(tracks)):
                        single_track = tracks[x].name
                        track_list.append(single_track)
                        x+=1
                if request.GET.get('name') in track_list:
                    return redirect('getTrackByName', name=request.GET.get('name'))
                else:
                    track = Track(name=request.GET.get('name'),track_id=pi, album=album)
                    track.save()
                    return redirect('getTrackByName', name=request.GET.get('name'))
        except ObjectDoesNotExist:
            album_response = requests.get('https://api.deezer.com/album/%s' %request.GET.get('album_id'))
            albums_data = album_response.json()
            if not albums_data.get('error'):
                try:
                    Artist.objects.get(artist_id=albums_data['contributors'][0]['id'])
                    artist = Artist.objects.get(artist_id=albums_data['contributors'][0]['id'])
                    if artist:
                        album = Album(name=albums_data['title'], album_id=albums_data['id'], artist= artist )
                        album.save()
                        track = Track(name=request.GET.get('name',track_id=pi, album=album))
                        track.save()
                        return redirect('getTrackByName', name=request.GET.get('name'))
                except ObjectDoesNotExist:
                    artist_response = requests.get('https://api.deezer.com/artist/%s' %albums_data['contributors'][0]['id'])
                    artists_data = artist_response.json()
                    artist = Artist(name=artists_data['name'], artist_id=artists_data['id'],link=artists_data['link'],tracklist=artists_data['tracklist'])
                    artist.save()
                    album = Album(name=albums_data['title'], album_id=albums_data['id'], artist= artist )
                    album.save()
                    track = Track(name=request.GET.get('name',track_id=pi, album=album))
                    track.save()
                    return redirect('getTrackByName', name=request.GET.get('name'))
            else:
                return HttpResponse('Album is not registered neither in API or Database.')
    return HttpResponse('The {{name}} param and the {{album_id}} param is required to associate track to album')

def updateTrack(request):
    try:
        Track.objects.get(track_id=request.GET.get('track_id'))
        track = Track.objects.get(track_id=request.GET.get('track_id'))
        track.name = request.GET.get('name')
        track.save()
        return redirect('getTrackById', id=request.GET.get('track_id'))
    except ObjectDoesNotExist:
        return HttpResponse('track_id was not found in the database, please check the correct id')

def deleteTrack(request):
    try:
        Track.objects.get(track_id=request.GET.get('track_id'))
        track = Track.objects.get(track_id=request.GET.get('track_id'))
        track.delete()
        return HttpResponse('Track Deleted')
    except ObjectDoesNotExist:
        return HttpResponse('track_id was not found in the database, please check the correct id')