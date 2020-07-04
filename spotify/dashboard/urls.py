from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('login/dashboard/', views.dashboard, name='dashboard'),
    path('login/dashboard/profile/', views.profile, name='profile'),
    path('login/dashboard/search/', views.search, name='search'),
    path('login/dashboard/artist/', views.artist, name='artist'),
    path('login/dashboard/album/', views.album, name='album'),
    path('login/dashboard/recommendation/', views.recommendation, name='recommendation'),
    path('login/dashboard/hiphop/', views.hiphop, name='hiphop'),
    path('login/dashboard/categories/', views.categories, name='categories'),
    path('login/dashboard/workout/', views.workout, name='workout'),
]