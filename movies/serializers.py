from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class MovieListSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    rating_user = serializers.BooleanField()
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user', 'rating')


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class RecursiveSerializer(serializers.Serializer):
    """для вывода рекурсивно children"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class ReviewSerializer(serializers.ModelSerializer):
    children = RecursiveSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')

class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    # reviews = serializers.SlugRelatedField(slug_field='text', read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)

class CreateRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip'),
            movie=validated_data.get('movie'),
            defaults={'star': validated_data.get("star")}
        )
        return rating
