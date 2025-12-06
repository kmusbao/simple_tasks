from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from getpass import getpass

class Command(BaseCommand):
    """Temporary solution. It creates new users and adds them to the database."""
    help = 'Create one or more users interactively'

    def handle(self, *args, **options):
        User = get_user_model()

        while True:
            username = input("Enter username (or leave empty to stop): ").strip()
            if not username:
                self.stdout.write(self.style.SUCCESS("Finished creating users."))
                break

            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"User '{username}' already exists."))
                continue

            password = getpass(f"Enter password for '{username}': ").strip()
            if not password:
                self.stdout.write(self.style.ERROR("Password cannot be empty."))
                continue

            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(f"User '{username}' created successfully."))
