from itertools import product

from django.core.serializers import serialize
from django.forms import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, MovieReviewSerializer
from .serializers import MovieValidateSerializer, DirectorValidateSerializer, ReviewValidateSerializer
from .serializers import MovieUpdateSerializer, DirectorUpdateSerializer, ReviewUpdateSerializer


@api_view(http_method_names=['GET', 'POST'])
def movie_list_api_view(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(instance=movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director_id')

        movie = Movie.objects.create(title=title, description=description, duration=duration, director_id=director_id)
        return Response(status=status.HTTP_201_CREATED, data=MovieSerializer(movie).data)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_api_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'ERROR': 'Movie not found'})

    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = MovieUpdateSerializer(data=request.data, context={'movie': movie})
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title', movie.title)
        description = serializer.validated_data.get('description', movie.description)
        duration = serializer.validated_data.get('duration', movie.duration)
        director_id = serializer.validated_data.get('director_id', movie.director_id)

        movie.title = title
        movie.description = description
        movie.duration = duration
        movie.director_id = director_id
        movie.save()
        return Response(status=status.HTTP_200_OK, data=MovieSerializer(movie).data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(http_method_names=['GET', 'POST'])
def director_list_api_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(instance=directors, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('name')
        director = Director.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED, data=DirectorSerializer(director).data)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_api_view(request, id):
    try:
        director = Director.objects.get(id=id)
    except Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'ERROR': 'Director not found'})

    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = DirectorUpdateSerializer(data=request.data, context={'director': director})
        serializer.is_valid(raise_exception=True)

        director.name = request.validated_data.get('name', director.name)
        director.save()
        return Response(status=status.HTTP_200_OK, data=DirectorSerializer(director).data)

    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(instance=reviews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = request.data.get('text')
        movie_id = request.data.get('movie_id')
        stars = request.data.get('stars')

        review = Review.objects.create(text=text, movie_id=movie_id, stars=stars)
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'ERROR': 'Review not found'})

    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ReviewUpdateSerializer(data=request.data, context={'review': review})
        serializer.is_valid(raise_exception=True)

        review.text = request.validated_data.get('text', review.text)
        review.movie_id = request.validated_data.get('movie_id', review.movie_id)
        review.stars = request.validated_data.get('stars', review.stars)

        review.save()
        return Response(status=status.HTTP_200_OK, data=ReviewSerializer(review).data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(http_method_names=['GET'])
def movie_review_list_api_view(request):
    movies = Movie.objects.all()
    serializer = MovieReviewSerializer(instance=movies, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)