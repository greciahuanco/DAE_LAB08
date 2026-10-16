from django.contrib import admin
from .models import Genre, Person, Movie, Rating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_date")
    search_fields = ("first_name", "last_name")


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "director")
    list_filter = ("release_year", "genres")
    search_fields = ("title",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [RatingInline]
    


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("movie", "score", "created_at")
    search_fields = ("movie__title",)