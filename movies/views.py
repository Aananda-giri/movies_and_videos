# some changes
import requests, urllib.parse
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from urllib3 import HTTPResponse
import json, os
# json.  
API_KEY = os.environ.get('TMDB_API_KEY');
BASE_URL = 'https://api.themoviedb.org/3';
API_URL = BASE_URL + '/discover/movie?sort_by=popularity.desc&'+API_KEY;
IMG_URL = 'https://image.tmdb.org/t/p/w500';
searchURL = BASE_URL + '/search/movie?' + API_KEY;


def home(request):
    # return render(request,'movies/home.html')
    # https://api.themoviedb.org/3/tv/top_rated?api_key=<<TMDB_API_KEY>>&language=en-US&page=1?adult=true
    trending_all = requests.get(BASE_URL + '/trending/all/week?api_key=' + API_KEY).json()['results']
    print(f'trending_all: \n\n {trending_all}')
    # trending_all = trending_all['results']
    # print(trending_all)
    popular_movie = requests.get(BASE_URL + '/movie/popular?api_key=' + API_KEY + '&language=en-US&page=1').json()['results']
    popular_series = requests.get(BASE_URL + '/tv/popular?api_key=' + API_KEY + '&language=en-US&page=1').json()['results']
    latest_movie = requests.get(BASE_URL + '/movie/now_playing?api_key=' + API_KEY + '&language=en-US&page=1').json()['results']
    latest_series = requests.get(BASE_URL + '/tv/on_the_air?api_key=' + API_KEY + '&language=en-US&page=1').json()['results']
    upcomming = requests.get(BASE_URL + '/movie/upcoming?api_key=' + API_KEY + '&language=en-US&page=1').json()['results']

    context = {'categories':['Trending', 'popular_movie', 'popular_series', 'latest_movie', 'upcomming'], 'values':{'Trending': trending_all, 'Popular Movies': popular_movie, 'Popular Series' : popular_series, 'Latest Movies': latest_movie, 'Latest Series': latest_series, 'Upcomming' : upcomming}}
    return render(request, 'movies/home.html', context)

def search(request):
    if request.method == 'GET':
        search_term = request.GET.get('search', None)
        print(f'search_term: {search_term}')
        genre =  request.GET.get('genre', None)
        genre_title =  request.GET.get('genre_title', None)
    
    if search_term !=None:
        search_term_parsed = urllib.parse.quote(search_term)
        print('\n\nsearch:',search_term_parsed)
        # t/p/w500/pHkKbIRoCe7zIFvqan9LFSaQAde.jpg
        search_results = requests.get(f'https://api.themoviedb.org/3/search/multi?api_key={API_KEY}&language=en-US&page=1&include_adult=true&query={search_term}').json()['results']
        # search_results = {'categories':['SEARCH : ' + str(search_term)], 'values':{'SEARCH {search_term} ' : search_results}}
        search_results = {'categories':[f'SEARCH <Movie> : {urllib.parse.unquote(search_term_parsed)}', f'SEARCH <MOVIE> : {urllib.parse.unquote(search_term_parsed)}'], 'values':{f'SEARCH : {urllib.parse.unquote(search_term_parsed)}' : search_results}, 'search_term' : search_term}
        # print('search_results',search_results)

    elif genre != None:
        print(f'genre: {genre}')
        genre_parsed = urllib.parse.quote(genre)
        # genre_title = urllib.parse.quote(genre_title)
        # t/p/w500/pHkKbIRoCe7zIFvqan9LFSaQAde.jpg
        search_results = requests.get(f'https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key={API_KEY}&with_genres={genre_parsed}').json()['results']
        # print(f'\n\n genre: {genre_parsed}\n genre_results', search_results)



        # print('search_genre\'', search_results ,'\'')
        search_results = {'categories':['SEARCH <Movie> : ' + str(genre), 'SEARCH <series> : ' + str(genre)], 'values':{'GENRE : ' + str(genre) : search_results}}
        print(search_term)
    # print(search_results)
    return render(request, 'movies/home.html', search_results)
    # return render(request, 'movies/search.html', search_results)
def series(request):
    # return render(request,'movies/movie.html')
    # http://127.0.0.1:8000/series/?tmdb_id=60573&season=5&episode=2
    if request.method == 'GET':
        tmdb_id = request.GET.get('tmdb_id')
        # what = request.GET.get('screen')
        # print(f'\n\ntmdb_id: {tmdb_id}, what: \'series\'\n\n')
        season = request.GET.get('season', None)
        episode = request.GET.get('episode', None)
        source = request.GET.get('source', None)
    if season == None or episode == None:
        season = 1
        episode = 1
    if source == None or int(source) == 1:
        
        movie_url = f'https://vidsrc.me/embed/{tmdb_id}/{season}-{episode}/'
        
        source = 1
    elif int(source) == 2:
        movie_url = f'https://2embed.org/embed/series?tmdb={tmdb_id}&s={season}&e={episode}'
    else:
        # https://seapi.link/?type=tmdb&id=85723&season=2&episode=1&max_results=1
        movie_url = requests.get(f"https://seapi.link/?type=tmdb&id={tmdb_id}&season={season}&episode={episode}&max_results=1").json()
        source = 3
        
        
    # 'https://api.themoviedb.org/3/tv/60573/season/1?api_key=<<TMDB_API_KEY>>&language=en-US'
    season_data = requests.get(f'https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season}?api_key={API_KEY}&language=en-US')
    print(season_data.json())
    
    # for similar series
    # https://api.themoviedb.org/3/tv/60573/similar?api_key=<<TMDB_API_KEY>>&language=en-US&page=1
    similar = requests.get(f'https://api.themoviedb.org/3/tv/{tmdb_id}/similar?api_key={API_KEY}&language=en-US&page=1').json()
    
    # https://api.themoviedb.org/3/tv/60573?api_key=<<TMDB_API_KEY>>&language=en-US
    # https://api.themoviedb.org/3/tv/60573/?season=6?episode=1/?api_key=<<TMDB_API_KEY>>&language=en-US
    # print(f'series_url: https://api.themoviedb.org/3/tv/{tmdb_id}?api_key=<<TMDB_API_KEY>>&language=en-US')
    # print(f'\n movie_url: {movie_url}')
    series_data = requests.get(f'https://api.themoviedb.org/3/tv/{tmdb_id}?api_key={API_KEY}&language=en-US').json()
    number_of_seasons = series_data['number_of_seasons']

    context = {'tmdb_id': tmdb_id, 'what': 'series', 'season_number': season, 'episode_number': int(episode), 'movie_url': movie_url, 'season_data': season_data.json(), 'number_of_seasons': number_of_seasons, 'stream' : 'series', 'source_index': source, 'series_data':series_data, 'similar': similar}
    # print(f'\n\n series:: context:{context}')
    # print(f'movie:{movie_url}')
    return render(request, 'movies/movie.html', context)
    # return HTTPResponse(str(context))

def movie(request):
    # return render(request,'movies/movie.html')
    # http://127.0.0.1:8000/movie/?tmdb_id=1726
    if request.method == 'GET':
        tmdb_id = request.GET.get('tmdb_id')
        source = request.GET.get('source', None)
        # what = request.GET.get('screen')
        # print(f'\n\ntmdb_id: {tmdb_id}, what: \'movie\'\n\n')

        
        if source == None or int(source) == 1:
            movie_url = f"https://vidsrc.me/embed/{tmdb_id}/"
            source = 1  # to avoid  sending 'none' to movie.html
            # for server in movie_url['results']:
            #     print(server['server'])
        elif int(source) == 2:
            movie_url = f'https://2embed.org/embed/movie?tmdb={tmdb_id}'
            
        else:
            # "https://seapi.link/?type=tmdb&id=634649&max_results=1"
            movie_url = requests.get(f"https://seapi.link/?type=tmdb&id={tmdb_id}&max_results=1").json()
            
            


        # https://api.themoviedb.org/3/movie/1726?api_key=<<TMDB_API_KEY>>&language=en-US
        movie_data = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={API_KEY}&language=en-US').json()
        # print('req_url: ', 'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=<<TMDB_API_KEY>>&language=en-US')

        # https://api.themoviedb.org/3/movie/1726/similar?api_key=<<TMDB_API_KEY>>&language=en-US&page=1
        similar = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}/similar?api_key={API_KEY}&language=en-US&page=1').json()

        # get actual movie info by tmdb id
        # movie_data = 
        # print(f'\n\nsource: {source}, movie_url: {movie_url}\n\n')
        context = {'tmdb_id':tmdb_id, 'what' : 'movie', 'movie_url': movie_url,'stream':'movie', 'source_index' : str(source) , 'series_data':movie_data, 'similar': similar}
        # print(f'\n\n context: {context}')
        return render(request,'movies/movie.html', context)
        # print(context)
        # return HTTPResponse(str('hi'))
    # context = {'movie_url' : ''}
    # return render(request, 'movies/movie.html', context=context)

def trailer(request):
    if request.method == 'GET':
        tmdb_id = request.GET.get('tmdb_id', None)
        what = request.GET.get('what', None)    # movie or series
        if what == 'movie':
            res = requests.get(f'https://api.themoviedb.org/3/movie/{tmdb_id}/videos?api_key={API_KEY}').json()
        else:
            res = requests.get(f'https://api.themoviedb.org/3/tv/{tmdb_id}/videos?api_key={API_KEY}').json()
        print(f'\n\ntmdb_id : {tmdb_id},  res: {res}')
        return JsonResponse(res)
    else:
        return JsonResponse({'error!' : 'require tmdb_id!! no \'tmdb_id\' provided!! '}, safe=False)

def country(request):
    # todo : movie by country
    return render(request, 'movies/country.html')

def genre(request):
    # todo : movie by genre
    return render(request, 'movies/search.html')

def top_imdb(request):
    # todo : top_imdb movies
    return render(request, 'movies/search.html')
