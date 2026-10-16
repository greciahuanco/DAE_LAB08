from django.core.management.base import BaseCommand, CommandError

from blog.duel.questions import BY_KEY
from blog.duel.runner import SOURCES, STATUS_LABEL, run_all


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--source", choices=sorted(SOURCES), default="team")
        parser.add_argument("--question", choices=sorted(BY_KEY))
        parser.add_argument("--strict", action="store_true")

    def handle(self, *args, **options):
        try:
            verdicts = run_all(options["source"], options["question"])
        except ModuleNotFoundError as exc:
            raise CommandError(str(exc)) from exc

        for verdict in verdicts:
            self.stdout.write(
                f"{verdict.key}  {STATUS_LABEL[verdict.status]:<24} {verdict.queries}"
            )
            if verdict.detail:
                self.stdout.write(verdict.detail)

        good = sum(verdict.status == "ok" for verdict in verdicts)
        self.stdout.write(f"{good}/{len(verdicts)}")
        if options["strict"] and good != len(verdicts):
            raise CommandError("duel")
