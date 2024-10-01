from django.core.management.base import BaseCommand, CommandError, CommandParser
from typing import Any

class Command(BaseCommand):
    help = "Say hello to the admins"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "say_hello", action="store_true"
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Hello cowboy!\n")

        return None