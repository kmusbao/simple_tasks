import pytest
from applications.job.models import Task
from applications.user.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_task_success():
    """
    Test for successful task creation.
    """
    user = User.objects.create_user(username="bob", password="123")
    client = APIClient()
    client.force_authenticate(user)

    payload = {
        "title": "Test",
        "description": "desc",
        "status": "todo",
        "due_date": "2025-12-10T10:00:00Z",
    }

    response = client.post("/tasks/", payload, format="json")

    assert response.status_code == 201
    assert response.data["title"] == "Test"
    assert Task.objects.count() == 1
    task = Task.objects.first()
    assert task.owner == user


@pytest.mark.django_db
def test_create_task_invalid_business_rule():
    """
    Test: Can't set status="done" without due_date
    """
    user = User.objects.create_user(username="bob", password="123")
    client = APIClient()
    client.force_authenticate(user)

    payload = {"title": "Invalid", "status": "done", "due_date": None}

    response = client.post("/tasks/", payload, format="json")

    assert response.status_code == 400
    assert "status" in response.data or "non_field_errors" in response.data


@pytest.mark.django_db
def test_cannot_delete_someone_elses_task():
    """
    Test: User cannot delete someone else task
    """
    owner = User.objects.create_user(username="alice", password="123")
    stranger = User.objects.create_user(username="bob", password="123")

    task = Task.objects.create(title="Mine", status="todo", owner=owner)

    client = APIClient()
    client.force_authenticate(stranger)

    response = client.delete(f"/tasks/{task.id}/")

    assert response.status_code in (403, 404)

    assert Task.objects.filter(id=task.id).exists()
