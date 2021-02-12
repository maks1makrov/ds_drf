from django.db.models import Sum, Count, Value, IntegerField
from django.db.models.functions import Cast
from django.shortcuts import render
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieListSerializer, MovieDetailSerializer, CreateReviewSerializer, \
    CreateRatingSerializer
from movies.service import get_client_ip


class TestView(View):
    def get(self, request):
        movies = Movie.objects.all()
        response = {}
        response['content'] = movies
        return render(request, "test.html", response)


# class MovieListView(ListAPIView):
#     serializer_class = MovieListSerializer
#
#     def get_queryset(self):
#         return Movie.objects.all()


class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(rating=(Sum('ratings__star') / Count("ratings"))).\
            annotate(rating_user=Count('ratings', filter='ratings__star' == get_client_ip(request)))
        serializer = MovieListSerializer(movies, many=True)
        print(get_client_ip(request))

        return Response(serializer.data)


class MovieDetailView(APIView):
    """детальная инфорация по фильму"""

    def get(self, request, id):
        movie = Movie.objects.get(id=id)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    def post(self, request):
        serializer = CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=201)


class CreateRatingView(APIView):

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
