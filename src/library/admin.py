from django.contrib import admin
from .models import Author, AuthorProfile, Book, Category, Publisher, Publication


admin.site.site_header = "Biblioteca - Laboratorio 4"
admin.site.site_title = "Administración de Biblioteca"
admin.site.index_title = "Gestión de Biblioteca"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "nationality")
    search_fields = ("first_name", "last_name")


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("author",)
    search_fields = ("author__first_name", "author__last_name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "publication_date")
    list_filter = ("author", "categories")
    search_fields = ("title", "isbn", "author__first_name", "author__last_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("book", "publisher", "edition", "publication_date")
    list_filter = ("publisher",)
    search_fields = ("book__title", "publisher__name")