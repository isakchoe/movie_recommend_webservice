from django.shortcuts import render
import requests
import random
from .models import Movie, Genre
from django.contrib.auth.decorators import login_required



def all_movies(n):
    movies = []
    page_list = list(range(1, n))  # 500개
    API_KEY = 'e2bee469ec06bfa8f505d5328b6ba499&language'

    for page in page_list:
        URL = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=ko-kr&page={page}'
        res = requests.get(URL).json()


        for movie in res['results']:
            temp = Movie.objects.create(
                        id = movie['id'],
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
        
            movies.append(movie)

    return movies


# 최종 배포시 
# movies = all_movies(6)


def recommend_random(request):
    movies = all_movies(6)

    random_movies = random.sample(movies, 3)

    context = {
        'recommend_movies': random_movies,
    }

    return render(request, 'movies/recommend_movies.html', context)



# 리뷰 기반 추천 
# 리뷰, 스코어, 스코어 점수로 나누어야한다. 
    #  1-10점,   7점 이상을 추천! 
    #  4점? 이하는 절대 추천 안함.
    # 사용자 -- user --> 리뷰를 역참조 
    # 리뷰 --> movie 역참조,, 
    # movie -- genre 테이블 역참조 확인,
    # sql -- join (리팩토링 개선) 
    # 장르에 맞게 필터링,, movies에서 장르 필터링, 
    #  평점이 높은순,,, 장르가 일치하는거,,, limit 추천 

@login_required
def recommend_review(request):
    movies = all_movies(6)

    user = request.user
    reviews = user.review_set.all()
    
    # 유저가 리뷰한 영화의 장르 
    pick_genres = []


    for review in reviews:
        # 리뷰가 7점이상이면 해당 장르를 추천, 
        if review.rate >= 7:
            movie = review.movie     
            genres = movie.genres.all()
            
        
            for genre in genres:
                pick_genres.append(genre.id)
    
    review_movies = []

    for movie in movies:
        for genre in movie['genre_ids']:

            if genre in pick_genres:
                count_score = 0 
                if movie['vote_count'] < 500:
                    count_score = 0 
                elif movie['vote_count'] < 2000:
                    count_score = 2 
                elif movie['vote_count'] < 5000:
                    count_score = 3
                elif movie['vote_count'] < 10000:
                    count_score = 4
                else:
                    count_score = 5
                
                result = movie['vote_average'] + count_score

                if result >=10:
                    review_movies.append([movie,result])


    
        
    
    # 3개 이상이면, 3개만 추리기! Result 높은순으로! 
    review_movies.sort(key=lambda x: -x[1])

    if len(review_movies) > 3:
        review_movies = review_movies[:3]

    new_review_movies = []
    for review_movie in review_movies:
        review_movie.pop()
        new_review_movies.append(review_movie[0])
        

    context ={
        'recommend_movies': new_review_movies,
    }


    return render(request, 'movies/recommend_movies.html', context)


def recommend(request):
    
    return render(request, 'movies/recommend.html')


def home(request):
    return render(request, 'movies/home.html')

# movie detail 
def detail(request, movie_pk):

    movie = Movie.objects.get(pk=movie_pk)
    print(movie_pk, movie.pk)
    
    context = {
        'movie': movie,
    }

    return render(request, 'movies/detail.html', context)