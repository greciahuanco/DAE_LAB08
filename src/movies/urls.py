from django.urls import path

from . import views


urlpatterns = [
    path(
        "movies/<int:movie_id>/recommendations/",
        views.movie_recommendations,
        name="movie_recommendations",
    ),
]