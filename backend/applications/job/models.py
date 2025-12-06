from applications.user.models import User
from django.db import models


class Task(models.Model):
    """
    Also known as a "task". This is useful for working in a company.
    """

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    TASK_STATUS_CHOICES = (
        (TODO, "Todo"),
        (IN_PROGRESS, "In progress"),
        (DONE, "Done"),
    )

    title = models.CharField(max_length=201, blank=True)
    description = models.CharField(max_length=1000, default="", blank=True)
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default=TODO
    )
    due_date = models.DateTimeField(db_index=True, null=True, blank=True)
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="tasks",
        on_delete=models.deletion.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_overdue = models.BooleanField(default=False)

    def __str__(self):
        return self.title
