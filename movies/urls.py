from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
    path('recommend/random/', views.recommend_random, name='recommend_random'),
    path('recommend/review/', views.recommend_review, name='recommend_review'),
]
