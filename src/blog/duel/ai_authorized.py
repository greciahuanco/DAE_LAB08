from datetime import date

from django.db.models import Count, Q

from blog.models import Author, Comment, Post


def q1():
    return Post.objects.filter(published=True)


def q2():
    return Post.objects.filter(category__isnull=True)


def q3():
    return Post.objects.filter(published=True).filter(
        published_at__gte=date(2026, 3, 1),
        published_at__lte=date(2026, 5, 31),
    )


def q4():
    return Post.objects.annotate(n_comments=Count("comments")).filter(n_comments__gt=2)


def q5():
    return (
        Post.objects.filter(published=True)
        .annotate(
            n_comments=Count("comments", distinct=True),
            n_tags=Count("tags", distinct=True),
        )
        .order_by("-n_comments", "pk")[:3]
    )


def q6():
    return Post.objects.filter(author__profile__country="Perú")


def q7():
    return Comment.objects.filter(post__category__name="Tecnología")


def q8():
    return Author.objects.filter(~Q(posts__published=True))
