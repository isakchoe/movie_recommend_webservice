from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('recommend/random/', views.recommend_random, name='recommend_random'),
    path('recommend/review/', views.recommend_review, name='recommend_review'),
]
