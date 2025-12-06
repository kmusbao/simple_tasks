from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=128, unique=True, blank=True)

    def __str__(self):
        return self.username
