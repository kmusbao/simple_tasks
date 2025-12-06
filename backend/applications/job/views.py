from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser

from .filters import TaskFilter
from .models import Task
from .permissions import IsOwner
from .serializers import TaskSerializer


@extend_schema_view(
    get=extend_schema(
        description="Retrieve all your tasks",
        responses={
            200: TaskSerializer, 404: {"description": "Your tasks not found."}
        },
    ),
    post=extend_schema(description="Create a new task", responses={
            201: TaskSerializer,
            400: {"description": "Validation error"},
        }
    ),
)
class TaskGetCreateView(generics.ListCreateAPIView):
    """View for creating new tasks and getting all those created by the user"""
    serializer_class = TaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema_view(
    get=extend_schema(
        description="Retrieve a task by ID",
        parameters=[
            OpenApiParameter(
                name="id", type=OpenApiTypes.INT, description="Task ID"
            )
        ],
        responses={
            200: TaskSerializer, 404: {"description": "Task not found."}
        },
    ),
    patch=extend_schema(
        description="Update a task by ID",
        request=TaskSerializer,
        responses={
            200: TaskSerializer, 404: {"description": "Task not found."}
        },
    ),
    delete=extend_schema(
        description="Delete a task by ID", responses={204: None}
    ),
)
class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    """View for getting a task by ID and updating its fields"""
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "id"

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
