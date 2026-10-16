from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse



class FrontPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_blog", verbosity=0)

    def test_front_page_shows_the_published_posts(self):
        response = self.client.get(reverse("front_page"))
        self.assertContains(response, "Introducción al ORM de Django")
        self.assertNotContains(response, "Borrador: migraciones")

    def test_front_page_runs_two_queries(self):

        with self.assertNumQueries(2):
            self.client.get(reverse("front_page"))
