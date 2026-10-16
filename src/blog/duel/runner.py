import importlib
from dataclasses import dataclass

from django.db import connection
from django.test.utils import CaptureQueriesContext

from .questions import QUESTIONS, Question



SOURCES = {
    "team": "blog.duel.team",
    "ai": "blog.duel.ai_answers",
    "ai_authorized": "blog.duel.ai_authorized",
    "solutions": "teacher.solutions",
}

STATUS_LABEL = {
    "ok": "✔ correcta",
    "costly": "⚠ correcta pero cara",
    "wrong": "✘ resultado distinto",
    "error": "✘ error",
    "todo": "· sin escribir",
}


@dataclass(frozen=True)
class Verdict:
    key: str
    status: str
    queries: int
    detail: str = ""


def _difference(got, expected) -> str:
    if isinstance(got, list) and isinstance(expected, list):
        if all(isinstance(item, str) for item in got + expected):
            missing = [item for item in expected if item not in got]
            extra = [item for item in got if item not in expected]
            parts = []
            if missing:
                parts.append(f"faltan {len(missing)} (p. ej. {missing[0]!r})")
            if extra:
                parts.append(f"sobran {len(extra)} (p. ej. {extra[0]!r})")
            if not parts:
                parts.append(f"mismos elementos pero {len(got)} filas contra {len(expected)}")
            return "; ".join(parts)
    return f"devolvió {got!r}; se esperaba {expected!r}"


def run_question(question: Question, answer) -> Verdict:
    try:
        with CaptureQueriesContext(connection) as captured:
            got = question.normalize(answer())
    except NotImplementedError:
        return Verdict(question.key, "todo", 0)
    except Exception as exc:
        return Verdict(question.key, "error", 0, f"{type(exc).__name__}: {exc}")
    queries = len(captured)
    if got != question.expected:
        return Verdict(question.key, "wrong", queries, _difference(got, question.expected))
    if queries > question.budget:
        return Verdict(
            question.key, "costly", queries,
            f"{queries} consultas; una buena respuesta necesita {question.budget}",
        )
    return Verdict(question.key, "ok", queries)


def run_all(source: str, only: str | None = None) -> list[Verdict]:
    module = importlib.import_module(SOURCES[source])
    verdicts = []
    for question in QUESTIONS:
        if only and question.key != only:
            continue
        answer = getattr(module, question.key, None)
        if answer is None:
            verdicts.append(Verdict(question.key, "todo", 0))
            continue
        verdicts.append(run_question(question, answer))
    return verdicts
