from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Movie, Director, Review


# ReviewSerializer
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text movie stars'.split()


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'.split()


# MovieSerializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title description duration director '.split()


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'.split()


# DirectorSerializer
class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, director):
        movies_count = director.movies.count()
        return movies_count


class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'.split()


class MovieReviewSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    review_name = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description duration director reviews review_name rating'.split()

    def get_review_name(self, movie):
        if movie.reviews.exists():
            return movie.reviews.first().text
        return None

    def get_rating(self, movie):
        reviews = movie.reviews.all()
        total_stars = sum(review.stars for review in reviews)
        count = reviews.count()
        return total_stars / count if count > 0 else 0


# Validate serializers
class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, min_length=3)
    description = serializers.CharField(max_length=100, min_length=3, required=False)
    duration = serializers.IntegerField(max_value=10, min_value=1)
    director_id = serializers.IntegerField(max_value=1000, min_value=1)

    def validate_title(self, title):
        if Movie.objects.filter(title=title).exists():
            raise serializers.ValidationError("Movie with this title already exists")
        return title

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except:
            raise serializers.ValidationError("Director does not exist")
        return director_id


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=3)
    director = serializers.CharField(max_length=100, min_length=3)

    def validate_name(self, name):
        if Director.objects.filter(name=name).exists():
            raise serializers.ValidationError("Director with this name already exists")
        return name


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=100, min_length=3)
    movie_id = serializers.IntegerField(max_value=1000, min_value=1)
    stars = serializers.IntegerField(max_value=5, min_value=1)

    def validate_text(self, text):
        if Review.objects.filter(text=text).exists():
            raise serializers.ValidationError("Review with this text already exists")
        return text

    def validate_movie_id(self, movie_id):
        try:
            Movie.objects.get(id=movie_id)
        except:
            raise serializers.ValidationError("Movie does not exist")
        return movie_id


class MovieUpdateSerializer(MovieValidateSerializer):
    def validate_title(self, title):
        movie = self.context.get('movie')
        if Movie.objects.filter(title__exact=title).exclude(id=movie.id).exists():
            raise ValidationError("Movie with this title already exists")
        return title

class DirectorUpdateSerializer(DirectorValidateSerializer):
    def validate_name(self, name):
        director = self.context.get('director')
        if Director.objects.filter(name_exact=name).exclude(id=director.id).exists():
            raise ValidationError("Director with this name already exists")
        return name

class ReviewUpdateSerializer(ReviewValidateSerializer):
    def validate_text(self, text):
        review = self.context.get('review')
        if Review.objects.filter(text_exact=text).exclude(id=review.id).exists():
            raise ValidationError("Review with this text already exists")
        return text