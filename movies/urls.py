from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend, name='recommend'),
    path('recommend/random/', views.recommend_random, name='recommend_random'),
    path('recommend/review/', views.recommend_review, name='recommend_review'),
    path('recommend/<int:movie_id>/', views.detail, name='detail'),
    path('recommend/search/', views.search_movies, name='search_movies'),
    path('recommend/<int:movie_id>/movie_reviews/', views.movie_reviews, name='movie_reviews'),
    path('recommend/<int:movie_api_id>/movie_reviews/', views.movie_reviews, name='movie_reviews'),
    path('recommend/delete_movies/', views.delete_movies, name="delete_movies"),
    path('recommend/insert_movies/', views.insert_movies, name="insert_movies"),
]
