from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from quiz.models import Choice, Question

from .helpers import seed


class ChoiceApiTests(APITestCase):
    def setUp(self):
        self.person, self.agent = seed()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.person}")
        self.question = Question.objects.first()

    def test_router_exposes_all_three_resources(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {"exams", "questions", "choices"})

    def test_choice_crud_returns_the_expected_status_codes(self):
        response = self.client.post(
            "/api/choices/",
            {"question": self.question.pk, "text": "Another option", "is_correct": False},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        url = f"/api/choices/{response.json()['id']}/"
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.patch(url, {"text": "Edited option"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "Edited option")
        response = self.client.put(
            url,
            {"question": self.question.pk, "text": "Replaced option", "is_correct": False},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertEqual(self.client.get(url).status_code, 404)
        self.assertEqual(self.question.choices.filter(is_correct=True).count(), 1)

    def test_creating_a_second_correct_choice_is_rejected(self):
        before = self.question.choices.count()
        response = self.client.post(
            "/api/choices/",
            {"question": self.question.pk, "text": "Another correct option", "is_correct": True},
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.question.choices.count(), before)
        self.assertEqual(self.question.choices.filter(is_correct=True).count(), 1)

    def test_updates_cannot_leave_zero_or_two_correct_choices(self):
        for choice in (
            self.question.choices.get(is_correct=True),
            self.question.choices.filter(is_correct=False).first(),
        ):
            with self.subTest(choice=choice.pk):
                response = self.client.patch(
                    f"/api/choices/{choice.pk}/",
                    {"is_correct": not choice.is_correct},
                    format="json",
                )
                self.assertEqual(response.status_code, 400)
                choice.refresh_from_db()
                self.assertEqual(self.question.choices.filter(is_correct=True).count(), 1)

    def test_the_correct_choice_cannot_be_deleted(self):
        choice = self.question.choices.get(is_correct=True)
        response = self.client.delete(f"/api/choices/{choice.pk}/")
        self.assertEqual(response.status_code, 400)
        self.assertTrue(Choice.objects.filter(pk=choice.pk).exists())

    def test_deletion_preserves_at_least_two_choices(self):
        choices = list(self.question.choices.filter(is_correct=False))
        for choice, expected in zip(choices, (204, 204, 400)):
            response = self.client.delete(f"/api/choices/{choice.pk}/")
            self.assertEqual(response.status_code, expected)
        self.assertEqual(self.question.choices.count(), 2)
        self.assertEqual(self.question.choices.filter(is_correct=True).count(), 1)

    def test_an_option_cannot_be_moved_to_another_question(self):
        choice = self.question.choices.filter(is_correct=False).first()
        other = Question.objects.exclude(pk=self.question.pk).first()
        response = self.client.patch(
            f"/api/choices/{choice.pk}/", {"question": other.pk}, format="json"
        )
        self.assertEqual(response.status_code, 400)
        choice.refresh_from_db()
        self.assertEqual(choice.question_id, self.question.pk)

    def test_invalid_question_identifiers_are_rejected(self):
        bodies = (
            {"text": "Option"},
            {"question": "invalid", "text": "Option"},
            {"question": 999999, "text": "Option"},
        )
        for body in bodies:
            with self.subTest(body=body):
                response = self.client.post("/api/choices/", body, format="json")
                self.assertEqual(response.status_code, 400)

    def test_choice_id_is_read_only(self):
        response = self.client.post(
            "/api/choices/",
            {"id": 999999, "question": self.question.pk, "text": "Another option"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.json()["id"], 999999)

    def test_contract_includes_the_choices_resource(self):
        response = self.client.get("/api/schema/", {"format": "json"})
        self.assertEqual(response.status_code, 200)
        paths = response.json()["paths"]
        self.assertIn("/api/choices/", paths)
        self.assertIn("/api/choices/{id}/", paths)

    def test_session_authentication_allows_browsing_all_three_resources(self):
        self.client.credentials()
        self.client.force_login(User.objects.get(username="profe"))
        for url in ("/api/", "/api/exams/", "/api/questions/", "/api/choices/"):
            with self.subTest(url=url):
                response = self.client.get(url, HTTP_ACCEPT="text/html")
                self.assertEqual(response.status_code, 200)
                self.assertIn("text/html", response["Content-Type"])
                self.assertContains(response, "rest_framework")

    def test_anonymous_choices_request_is_unauthorized(self):
        self.client.credentials()
        self.assertEqual(self.client.get("/api/choices/").status_code, 401)
