import json

from django.core.management.base import BaseCommand, CommandError

from blog.agent.registry import execute


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--intent", required=True)
        parser.add_argument("--approve")

    def handle(self, *args, **options):
        try:
            intent = json.loads(options["intent"])
        except json.JSONDecodeError as exc:
            raise CommandError(str(exc)) from exc

        result = execute(intent, options["approve"])
        self.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
