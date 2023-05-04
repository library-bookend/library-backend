from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    blocked_until = models.DateTimeField(null=True, default=None)
    is_employee = models.BooleanField(default=False)
    STATUS_CHOICES = (
        ('blocked', 'Blocked'),
        ('active', 'Active'),

    )
    status = models.CharField(max_length=10, choices= STATUS_CHOICES, default='active')
