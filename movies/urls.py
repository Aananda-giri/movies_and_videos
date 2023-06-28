from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('movies/', list_movies, name='movies'),    # list movies page
    path('series/', list_series, name='series'),    # list series pageqq
    path('movie/', movie, name='movie'),    # watch movie page
    path('series/', series, name='series'), # watch series page
    path('trailer/', trailer, name='trailer'),
    path('country/', country, name='country'),
    path('genre/', genre, name='genre'),
    path('top_imdb', top_imdb, name='top_imdb'),
]