import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable

from django.db import transaction
from django.db.models import Count

from blog.models import Comment, Post


@dataclass(frozen=True)
class Action:
    name: str
    risk: str
    params: dict[str, type]
    run: Callable[..., Any]
    plan: Callable[..., dict] | None = None





def _posts_by_category(category: str):
    posts = Post.objects.filter(category__name=category).values("id", "title")
    return list(posts)


def _comments_of_post(post_id: int):
    return list(Comment.objects.filter(post_id=post_id).values("author_name", "text"))


def _posts_per_author():
    rows = Post.objects.values("author__name").annotate(total=Count("id")).order_by("-total")
    return [{"author": row["author__name"], "total": row["total"]} for row in rows]





def _plan_delete_comments(post_id: int) -> dict:
    ids = list(Comment.objects.filter(post_id=post_id).order_by("id").values_list("id", flat=True))
    return {"affected_comment_ids": ids}


def _delete_comments(post_id: int):
    with transaction.atomic():
        deleted, _ = Comment.objects.filter(post_id=post_id).delete()
    return {"deleted": deleted}


ACTIONS: dict[str, Action] = {
    action.name: action
    for action in (
        Action("posts_by_category", "R0", {"category": str},
               _posts_by_category),
        Action("comments_of_post", "R0", {"post_id": int},
               _comments_of_post),
        Action("posts_per_author", "R0", {},
               _posts_per_author),
        Action("delete_comments_of_post", "R2", {"post_id": int},
               _delete_comments,
               plan=_plan_delete_comments),
    )
}





def _denied(reason: str) -> dict:
    return {"status": "denied", "reason": reason}


def _valid_args(action: Action, args: Any) -> str | None:
    if not isinstance(args, dict):
        return "args must be an object"
    if set(args) != set(action.params):
        return f"expected arguments {sorted(action.params)}, got {sorted(args)}"
    for name, kind in action.params.items():
        value = args[name]

        if not isinstance(value, kind) or isinstance(value, bool):
            return f"argument {name!r} must be {kind.__name__}"
    return None


def plan_hash(action: Action, args: dict, details: dict) -> str:
    canonical = json.dumps(
        {"action": action.name, "args": args, "details": details}, sort_keys=True
    )
    return hashlib.sha256(canonical.encode()).hexdigest()[:12]


def execute(intent: Any, approval: str | None = None) -> dict:
    if not isinstance(intent, dict):
        return _denied("the intent must be an object")
    action = ACTIONS.get(intent.get("action"))
    if action is None:
        return _denied(f"unknown action {intent.get('action')!r}")
    args = intent.get("args", {})
    problem = _valid_args(action, args)
    if problem:
        return _denied(problem)

    if action.risk == "R0":
        return {"status": "ok", "untrusted_data": action.run(**args)}



    details = action.plan(**args)
    digest = plan_hash(action, args, details)
    plan = {"action": action.name, "args": args, "details": details, "plan_hash": digest}
    if approval != digest:
        return {"status": "approval_required", "plan": plan}
    return {"status": "applied", "plan": plan, "result": action.run(**args)}
