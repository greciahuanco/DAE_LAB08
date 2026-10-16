from django.core.management import call_command
from django.test import TestCase

from blog import seed_data
from blog.models import Author, Comment, Post


class SeedTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_blog", verbosity=0)

    def test_counts_match_the_seed_data(self):
        self.assertEqual(Author.objects.count(), len(seed_data.AUTHORS))
        self.assertEqual(Post.objects.count(), len(seed_data.POSTS))
        expected_comments = sum(p["comments"] for p in seed_data.POSTS)
        self.assertEqual(Comment.objects.count(), expected_comments)

    def test_seeding_twice_does_not_duplicate(self):
        original_ids = list(Post.objects.order_by("id").values_list("id", flat=True))
        call_command("seed_blog", verbosity=0)
        self.assertEqual(Post.objects.count(), len(seed_data.POSTS))
        self.assertEqual(
            list(Post.objects.order_by("id").values_list("id", flat=True)),
            original_ids,
        )

    def test_the_hostile_comment_is_there(self):
        self.assertTrue(Comment.objects.filter(text=seed_data.HOSTILE_COMMENT).exists())
