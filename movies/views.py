from django.shortcuts import render
import requests
import random


def all_movies(n):
    movies = []
    page_list = list(range(1, n))  # 500개
    API_KEY = 'e2bee469ec06bfa8f505d5328b6ba499&language'

    for page in page_list:
        URL = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=ko-kr&page={page}'
        res = requests.get(URL).json()

        for movie in res['results']:
            movies.append(movie)

    return movies


def recommend_random(request):
    movies = all_movies(6)
    random_movies = random.sample(movies, 10)

    context = {
        'random_movies': random_movies,
    }

    return render(request, 'movies/recommend_movies.html', context)


def index(request):
    
    return render(request, 'movies/index.html')