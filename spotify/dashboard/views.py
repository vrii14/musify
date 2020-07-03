from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests


def dashboard(response):
    return render(response, "dashboard/dashboard.html")


def profile(response):
    return render(response, "dashboard/profile.html")

def search(response):
    return render(response, "dashboard/search.html")

def artist(response):
    return render(response, "dashboard/artist.html")

def album(response):
    return render(response, "dashboard/album.html")
