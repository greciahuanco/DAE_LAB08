from datetime import date

from django.core.management import call_command
from django.db.models import QuerySet
from django.test import TestCase

from blog.duel import team
from blog.duel.questions import BY_KEY
from blog.duel.runner import run_all
from blog.models import Author, Post


class DuelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_blog", verbosity=0)

    def test_all_queries_match_the_oracle_with_one_query(self):
        for key in BY_KEY:
            with self.subTest(question=key):
                answer = getattr(team, key)()
                self.assertIsInstance(answer, QuerySet)
                with self.assertNumQueries(1):
                    result = BY_KEY[key].normalize(answer)
                self.assertEqual(result, BY_KEY[key].expected)
                if key == "q5":
                    self.assertEqual(len(answer), 3)
                verdict = run_all("team", only=key)[0]
                self.assertEqual(verdict.status, "ok")
                self.assertEqual(verdict.queries, 1)

    def test_q3_includes_boundary_dates_and_excludes_unpublished_posts(self):
        draft = Post.objects.create(
            title="Draft",
            author=Author.objects.first(),
            published=False,
            published_at=date(2026, 4, 1),
        )
        result = team.q3()
        dates = set(result.values_list("published_at", flat=True))
        self.assertIn(date(2026, 3, 1), dates)
        self.assertIn(date(2026, 5, 31), dates)
        self.assertNotIn(date(2026, 2, 28), dates)
        self.assertNotIn(date(2026, 6, 1), dates)
        self.assertFalse(result.filter(pk=draft.pk).exists())
