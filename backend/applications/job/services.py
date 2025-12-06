# tasks/services.py
from django.db.models import Q
from django.utils import timezone

from .models import Task


def recalculate_overdue_tasks(user=None):
    """A script to update overdue tasks"""
    qs = Task.objects.filter(owner=user)

    now = timezone.now()

    overdue = qs.filter(due_date__lt=now, status__in=["todo", "in_progress"])
    overdue.update(is_overdue=True)

    not_overdue = qs.filter(Q(due_date__gte=now) | Q(status="done"))
    not_overdue.update(is_overdue=False)
