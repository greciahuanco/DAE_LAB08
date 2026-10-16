from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Any

from blog import seed_data

POSTS = seed_data.POSTS
COUNTRY_OF = dict(seed_data.AUTHORS)


@dataclass(frozen=True)
class Question:
    key: str
    expected: Any
    normalize: Callable[[Any], Any]
    budget: int = 1


def _titles(posts):
    return sorted(post.title for post in posts)


def _expected_top_three():
    published = [p for p in POSTS if p["published"]]
    ranked = sorted(published, key=lambda p: -p["comments"])[:3]
    return [(p["title"], p["comments"], len(p["tags"])) for p in ranked]


def _expected_authors_without_published():
    published_by = {p["author"] for p in POSTS if p["published"]}
    return sorted(name for name, _ in seed_data.AUTHORS if name not in published_by)


QUESTIONS = [
    Question(
        key="q1",
        expected=sorted(p["title"] for p in POSTS if p["published"]),
        normalize=_titles,
    ),
    Question(
        key="q2",
        expected=sorted(p["title"] for p in POSTS if p["category"] is None),
        normalize=_titles,
    ),
    Question(
        key="q3",
        expected=sorted(
            p["title"] for p in POSTS
            if p["date"] is not None and date(2026, 3, 1) <= p["date"] <= date(2026, 5, 31)
        ),
        normalize=_titles,
    ),
    Question(
        key="q4",
        expected=sorted(p["title"] for p in POSTS if p["comments"] > 2),
        normalize=_titles,
    ),
    Question(
        key="q5",
        expected=_expected_top_three(),
        normalize=lambda posts: [(p.title, p.n_comments, p.n_tags) for p in list(posts)[:3]],
    ),
    Question(
        key="q6",
        expected=sorted(p["title"] for p in POSTS if COUNTRY_OF[p["author"]] == "Perú"),
        normalize=_titles,
    ),
    Question(
        key="q7",
        expected=sorted(
            text
            for p in POSTS if p["category"] == "Tecnología"
            for _author, text in seed_data.comments_of(p)
        ),
        normalize=lambda comments: sorted(c.text for c in comments),
    ),
    Question(
        key="q8",
        expected=_expected_authors_without_published(),
        normalize=lambda authors: sorted(a.name for a in authors),
    ),
]

BY_KEY = {question.key: question for question in QUESTIONS}
