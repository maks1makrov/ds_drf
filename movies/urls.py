from django.urls import path

from movies import views

urlpatterns = [
    path("test/", views.TestView.as_view()),
    path("movie/", views.MovieListView.as_view()),
    path("movie/<int:id>", views.MovieDetailView.as_view()),
    path("review", views.ReviewCreateView.as_view()),
    path('rating', views.CreateRatingView.as_view()),

]


