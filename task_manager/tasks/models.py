from django.db import models
from django.conf import settings
from task_manager.statuses.models import Status

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='authored_task',
        on_delete=models.PROTECT
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='executed_task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
