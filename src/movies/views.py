from django.db.models import Avg
from django.shortcuts import get_object_or_404, render

from .models import Movie


def movie_recommendations(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    recommendations = (
        Movie.objects.filter(genres__in=movie.genres.all())
        .exclude(id=movie.id)
        .annotate(average_rating=Avg("ratings__score"))
        .order_by("-average_rating")
        .distinct()
    )

    context = {
        "movie": movie,
        "recommendations": recommendations,
    }

    return render(request, "movies/recommendations.html", context)