from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='authored_tasks',
        on_delete=models.PROTECT
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tasks',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    created_at=models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)