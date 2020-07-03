from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('login/dashboard/', views.dashboard, name='dashboard'),
    path('login/dashboard/profile/', views.profile, name='profile'),
    path('login/dashboard/search/', views.search, name='search'),
    path('login/dashboard/artist/', views.artist, name='artist'),
    path('login/dashboard/album/', views.album, name='album'),
]