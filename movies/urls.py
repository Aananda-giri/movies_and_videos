from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('movie/', movie, name='movie'),
    path('series/', series, name='series'),
    path('trailer/', trailer, name='trailer'),
    path('country/', country, name='country'),
    path('genre/', genre, name='genre'),
    path('top_imdb', top_imdb, name='top_imdb'),
]