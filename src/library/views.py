from django.shortcuts import render, get_object_or_404
from .models import Book


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    publications = book.publication_set.select_related('publisher').all()
    context = {
        'book': book,
        'publications': publications,
    }
    return render(request, 'library/book_detail.html', context)