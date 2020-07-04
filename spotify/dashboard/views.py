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


def profile(response):
    return render(response, "dashboard/profile.html")

def search(response):
    return render(response, "dashboard/search.html")

def artist(request):
    r = {}
    if request.method == "GET":
            search_term =  request.GET.get('search', 'default')
            r = spotify.client.get_artist(search_term)
            print(r)
            return render(request, 'dashboard/artist.html', {'data': r, "flag": "search"})

def album(response):
    return render(response, "dashboard/album.html")

def recommendation(response):
    return render(response, "dashboard/recommendation.html")

def categories(response):
    return render(response, "dashboard/categories.html")


def hiphop(response):
    return render(response, "dashboard/hiphop.html")
