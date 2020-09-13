from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, related_name='task_user', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(blank=True, default=False)
    description = models.fields.TextField(null=False, blank=False)
