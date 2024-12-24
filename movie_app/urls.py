from django.urls import path
from movie_app import views

urlpatterns = [
    path('movie_class/', views.MovieListAPIView.as_view(), name='movie_list'),
    path('movie_class/<int:id>/', views.MovieDetaiglAPIView.as_view(), name='movie_detail'),
    path('director_class/', views.DirectorListAPIView.as_view(), name='director_list'),
    path('director_class/<int:id>/', views.DirectorDetailAPIView.as_view(), name='director_detail'),
    path('review_class/', views.ReviewListAPIView.as_view(), name='review_list'),
    path('review_class/<int:id>/', views.ReviewDetailAPIView.as_view(), name='review_detail'),
]