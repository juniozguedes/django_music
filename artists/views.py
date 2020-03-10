import json
import random
import string
import requests
from .models import Artist
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

def getArtists(request):
    artists = Artist.objects.all()
    data = {"results": list(artists.values("artist_id", "name"))}
    return JsonResponse(data)
    
def getArtistByName(request, name):
    try: 
        Artist.objects.get(name__icontains=name)
        artists = Artist.objects.filter(name__icontains=name)
        data = {"results": list(artists.values("artist_id", "name"))}
        return JsonResponse(data)
    except ObjectDoesNotExist:
        response = requests.get('https://api.deezer.com/search/artist?q=%s' %name)
        artists_data = response.json()
        if artists_data.get('total') == 0:
            return HttpResponse('No artist according to URL param Name')
        else:
            artist = Artist(name=artists_data['data'][0]['name'], artist_id=artists_data['data'][0]['id'],link=artists_data['data'][0]['link'],tracklist=artists_data['data'][0]['tracklist'])
            artist.save()
            return redirect('getArtistByName', name=artist.name)

def getArtistById(request, id):
    try: 
        Artist.objects.get(artist_id=id)
        artists = Artist.objects.filter(artist_id=id)
        data = {"results": list(artists.values("artist_id", "name"))}
        return JsonResponse(data)
    except ObjectDoesNotExist:
        response = requests.get('https://api.deezer.com/artist/%s' %id)
        artists_data = response.json()
        if artists_data.get('error'):
            return HttpResponse('No artist according to URL param ID')
        else:
            artist = Artist(name=artists_data['name'], artist_id=artists_data['id'],link=artists_data['link'],tracklist=artists_data['tracklist'])
            artist.save()
            return redirect('getArtistById', id=artists_data['id'])

def addArtist(request):
    N = 27
    pi = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    if request.GET.get('name'):
        try:
            Artist.objects.get(name__icontains=request.GET.get('name'))
            artists = Artist.objects.filter(name__icontains=request.GET.get('name'))
            data = {"results": list(artists.values("artist_id", "name"))}
            return JsonResponse(data)
        except ObjectDoesNotExist:
            response = requests.get('https://api.deezer.com/search/artist?q=%s' %request.GET.get('name'))
            artists_data = response.json()
            if artists_data.get('total') == 0:
                artist = Artist(name=request.GET.get('name'), artist_id=pi ,link='Not available on Deezer',tracklist='Not available on Deezer')
                artist.save()
                return redirect('getArtistByName', name=artist.name)
            elif artists_data['data'][0]['name'] == request.GET.get('name'):
                return redirect('getArtistByName', name=request.GET.get('name'))
            else:    
                artist = Artist(name=request.GET.get('name'), artist_id=pi ,link='Not available on Deezer',tracklist='Not available on Deezer')
                artist.save()
                return redirect('getArtistByName', name=artist.name)
    else:
        return HttpResponse('Passar o nome do artista como parâmetro "name" para ser cadastrado Ex.: 0.0.0.0:8000/artists/add/?name=Crocker rock')

def updateArtist(request):
    try:
        Artist.objects.get(artist_id=request.GET.get('artist_id'))
        artist = Artist.objects.get(artist_id=request.GET.get('artist_id'))
        artist.name = request.GET.get('name')
        artist.save()
        return redirect('getArtistByName', name=artist.name)
    except ObjectDoesNotExist:
        return HttpResponse('artist_id was not found in the database, please check the correct id')

def deleteArtist(request):
    try:
        Artist.objects.get(artist_id=request.GET.get('artist_id'))
        artist = Artist.objects.get(artist_id=request.GET.get('artist_id'))
        artist.delete()
        return HttpResponse('Artist Deleted')
    except ObjectDoesNotExist:
        return HttpResponse('artist_id was not found in the database, please check the correct id')