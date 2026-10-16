from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def home(request):
    articles = Article.objects.all().order_by("-publication_date")
    return render(request, "news/home.html", {"articles": articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "news/article_detail.html", {"article": article})


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    articles = category.articles.all().order_by("-publication_date")

    context = {
        "category": category,
        "articles": articles,
    }

    return render(request, "news/category_list.html", context)