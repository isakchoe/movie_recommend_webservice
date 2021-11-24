from django.shortcuts import redirect, render
import requests
import random
from .models import Movie, Genre
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Max

def all_movies(n):
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
        
            movies.append(temp)

    # 디비가 아니라 tmdb api(movie_api_id가 없다 )
    return movies


def delete_movies(request):
    # 삭제 
    movies = Movie.objects.all()
    for movie in movies:
        movie.delete()
    return redirect('movies:recommend')


def insert_movies(request):
    # db 저장 
    all_movies(6)
    return redirect('movies:recommend')


def recommend_random(request):

    random_movies = Movie.objects.order_by('?')[:3]

    context = {
        'recommend_movies': random_movies,
    }

    return render(request,'movies/recommend_movies.html', context)



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

    user = request.user
    reviews = user.review_set.all()
    
    # 유저가 리뷰한 영화의 장르 
    pick_genres = []
    pick_movies = {}


    for review in reviews:
        # 리뷰가 7점이상이면 해당 장르를 추천, 
        if review.rate >= 7:
            movie = review.movie

            # 사용자가 리뷰한 영화 따로 저장
            if movie.title not in pick_movies:
                pick_movies[movie.title] = 1
            
            genres = movie.genres.all()
            
            for genre in genres:
                pick_genres.append(genre.id)
    
    review_movies = set()
    movies = Movie.objects.all()

    for movie in movies:
        # 이미 사용자가 리뷰한 영화라면 스킵 
        if movie.title in pick_movies:
            continue
        genres = movie.genres.all()

        for genre in genres:
            if genre.id in pick_genres:
                count_score = 0 
                if movie.vote_count < 500:
                    count_score = 0 
                elif movie.vote_count < 2000:
                    count_score = 1
                elif movie.vote_count < 5000:
                    count_score = 1.5
                elif movie.vote_count < 10000:
                    count_score = 2
                else:
                    count_score = 2.5
                
                result = movie.vote_average + count_score

                if result >=10:
                    review_movies.add((movie,result))
    # set --> list 
    review_movies = list(review_movies)
    new_review_movies = []

    # 빈배열 아니면, 정렬
    if review_movies:
        review_movies.sort(key=lambda x: -x[1])
        # 3개 이상이면, 3개만 추리기! Result 높은순으로! 
        if len(review_movies) > 3:
            review_movies = review_movies[:3]
            for movie, result_score in review_movies:
                new_review_movies.append(movie)
    

    context ={
        'recommend_movies': new_review_movies,
        'msg':'추천결과',
    }

    return render(request, 'movies/recommend_movies.html', context)


def recommend(request):
    return render(request, 'movies/recommend.html')


count = 0 

def home(request):
    global count
    if count == 0:
        movies = all_movies(6)
        random_movies = random.sample(movies, 3)
        count += 1
    
    else:
        random_movies = Movie.objects.order_by('?')[:3]
    
    context = {
        'first_movie': random_movies[0],
        'sec_movie' : random_movies[1],
        'third_movie': random_movies[2],
    }
    
    return render(request, 'movies/home.html', context)

# movie detail 
def detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_api_id=movie_id)
    
    context = {
        'movie': movie,
    }

    return render(request, 'movies/detail.html', context)


# ㅇㅕㅇ호ㅏ  검검색  
def search_movies(request):
    search = request.GET.get('data')
    
    # django orm 
    movies = Movie.objects.filter(title__contains=search)[:3]

    context ={
        'recommend_movies': movies,
        'msg':'검색결과',
    }
    return render(request,'movies/recommend_movies.html',context)


def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, movie_api_id=movie_id)
    
    # 영화에서 리뷰 역참조
    reviews_of_movie = movie.review_set.all()
    
    paginator = Paginator(reviews_of_movie, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'community/index.html', context)

