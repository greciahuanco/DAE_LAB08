from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
]