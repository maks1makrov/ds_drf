from django.shortcuts import render
from django.views import View
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieListSerializer, MovieDetailSerializer


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
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """детальная инфорация по фильму"""
    def get(self, request, id):
        movie = Movie.objects.get(id=id)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
