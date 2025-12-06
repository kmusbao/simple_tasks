from applications.job.services import recalculate_overdue_tasks
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Recalculate overdue tasks for all users"

    def handle(self, *args, **options):
        for user in User.objects.all():
            recalculate_overdue_tasks(user)
        self.stdout.write(self.style.SUCCESS("Overdue tasks recalculated"))
