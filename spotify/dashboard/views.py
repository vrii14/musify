from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import requests
from . import spotify 

def dashboard(response):
    return render(response, "dashboard/dashboard.html")


def profile(request):
    r = {}
    search_term = ""
    if request.method == "GET":
        search_term =  request.GET.get('search', '  ')
        if (search_term != ""):
            r = spotify.client.get_user_data(search_term)
            return render(request, 'dashboard/profile.html', {'r': r, "flag": "search"})
        else:
            return HttpResponse("Input a value")


def search(request):
    r = {}
    if request.method == "GET":
        query =  request.GET.get('q','  ')
        type_q = request.GET.get('type', '  ')
        r = spotify.client.search(query, type_q)
        type_q = type_q.lower()
        return render(request, 'dashboard/search.html', {'r': r, "flag": "search", 'type_q': type_q})
        
def artist(request):
    r = {}
    search_term = ""
    if request.method == "GET":
        search_term =  request.GET.get('search','  ')
        if (search_term != ""):
            r = spotify.client.get_artist(search_term)
            return render(request, 'dashboard/artist.html', {'r': r, "flag": "search"})
        else:
            return HttpResponse("Input a value")

def album(request):
    r = {}
    search_term = ""
    if request.method == "GET":
        search_term =  request.GET.get('search', '  ')
        if (search_term != ""):
            r = spotify.client.get_album(search_term)
            return render(request, 'dashboard/album.html', {'r': r, "flag": "search"})
        else:
            return HttpResponse("Input a value")

def recommendation(request):
    r = {}
    if request.method == "GET":
        track_name =  request.GET.get('track','  ')
        artist_name = request.GET.get('artist', '  ')
        track_id = spotify.client.get_track_id(track_name)
        artist_id = spotify.client.get_artist_id(artist_name)
        r = spotify.client. get_recommendations(artist_id, None, track_id)
        return render(request, 'dashboard/recommendation.html', {'r': r, "flag": "search"})

def categories(response):
    r = spotify.client.get_list_of_categories()
    return render(response, "dashboard/categories.html", {'data':r})


def hiphop(response):
    r = spotify.client.get_a_category_playlist('hiphop')
    r = r['playlists']['items']
    return render(response, "dashboard/hiphop.html", {'data':r})

def workout(response):
    r = spotify.client.get_a_category_playlist('workout')
    r = r['playlists']['items']
    return render(response, "dashboard/workout.html", {'data':r})
