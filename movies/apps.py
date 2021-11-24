
import requests
import django
django.setup()
from django.apps import AppConfigs
from .models import Movie

class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'


    def ready(self):
        movies = []
        page_list = list(range(1, n))  # 500개
        API_KEY = 'e2bee469ec06bfa8f505d5328b6ba499&language'

        for page in page_list:
            URL = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=ko-kr&page={page}'
            res = requests.get(URL).json()

            for movie in res['results']:
                # 디비에 저장 
                temp = Movie.objects.create(
                            movie_api_id = movie['id'],
                            title = movie['title'],
                            release_date = movie['release_date'],
                            popularity = movie['popularity'],
                            vote_count = movie['vote_count'],
                            vote_average = movie['vote_average'],
                            overview = movie['overview'],
                            poster_path = movie['poster_path'],
                        )

                for genre_id in movie['genre_ids']:
                    temp.genres.add(genre_id)
        

