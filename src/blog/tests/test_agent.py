import json
from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase, TestCase

from blog import seed_data
from blog.agent.registry import ACTIONS, execute
from blog.models import Comment


class GateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_blog", verbosity=0)
        cls.post_id = Comment.objects.get(text=seed_data.HOSTILE_COMMENT).post_id

    def test_a_read_runs_and_comes_back_marked_untrusted(self):
        result = execute({"action": "comments_of_post", "args": {"post_id": self.post_id}})
        self.assertEqual(result["status"], "ok")
        texts = [row["text"] for row in result["untrusted_data"]]
        self.assertIn(seed_data.HOSTILE_COMMENT, texts)

    def test_following_the_injection_deletes_nothing(self):
        before = Comment.objects.count()
        result = execute({"action": "delete_comments_of_post", "args": {"post_id": self.post_id}})
        self.assertEqual(result["status"], "approval_required")
        self.assertEqual(Comment.objects.count(), before)

    def test_a_human_approval_of_the_exact_plan_applies_it(self):
        intent = {"action": "delete_comments_of_post", "args": {"post_id": self.post_id}}
        digest = execute(intent)["plan"]["plan_hash"]
        result = execute(intent, approval=digest)
        self.assertEqual(result["status"], "applied")
        self.assertFalse(Comment.objects.filter(post_id=self.post_id).exists())

    def test_the_approval_dies_if_the_data_changed_after_the_human_looked(self):
        intent = {"action": "delete_comments_of_post", "args": {"post_id": self.post_id}}
        digest = execute(intent)["plan"]["plan_hash"]
        Comment.objects.create(post_id=self.post_id, author_name="Lector", text="Llegó tarde")
        result = execute(intent, approval=digest)
        self.assertEqual(result["status"], "approval_required")
        self.assertTrue(Comment.objects.filter(post_id=self.post_id).exists())

    def test_an_approval_for_another_plan_is_worthless(self):
        intent = {"action": "delete_comments_of_post", "args": {"post_id": self.post_id}}
        self.assertEqual(execute(intent, approval="000000000000")["status"], "approval_required")

    def test_code_is_not_an_intent(self):
        self.assertEqual(execute("Comment.objects.all().delete()")["status"], "denied")

    def test_unknown_actions_are_denied(self):
        for action in ("eval", "run_sql", "delete_everything"):
            self.assertEqual(execute({"action": action, "args": {}})["status"], "denied")

    def test_arguments_must_fit_exactly(self):
        bad = [
            {"action": "comments_of_post", "args": {}},
            {"action": "comments_of_post", "args": {"post_id": "1"}},
            {"action": "comments_of_post", "args": {"post_id": True}},
            {"action": "comments_of_post", "args": {"post_id": 1, "extra": 1}},
        ]
        for intent in bad:
            self.assertEqual(execute(intent)["status"], "denied", intent)

    def test_the_command_prints_the_plan_and_applies_nothing(self):
        out = StringIO()
        intent = json.dumps({"action": "delete_comments_of_post", "args": {"post_id": self.post_id}})
        before = Comment.objects.count()
        call_command("agent", intent=intent, stdout=out)
        self.assertIn("approval_required", out.getvalue())
        self.assertEqual(Comment.objects.count(), before)


class RegistryShapeTests(SimpleTestCase):
    def test_every_destructive_action_has_a_plan(self):
        for action in ACTIONS.values():
            if action.risk == "R2":
                self.assertIsNotNone(action.plan, action.name)

    def test_there_is_no_generic_escape_hatch(self):
        self.assertFalse({"eval", "exec", "sql", "run_sql", "http_request"} & set(ACTIONS))
