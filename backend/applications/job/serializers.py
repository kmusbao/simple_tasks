from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Rule: If status becomes 'done', the task must have a due_date.
        """
        new_status = data.get("status", getattr(self.instance, "status", None))

        if new_status == "done":
            due = data.get(
                "due_date", getattr(self.instance, "due_date", None)
            )
            if due is None:
                raise serializers.ValidationError(
                    {
                        "status": "Cannot set status to 'done'. "
                                  "The task must have a due_date."
                    }
                )

        return data

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "owner",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("owner", "created_at", "updated_at")