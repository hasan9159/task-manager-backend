# activity/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class ActivityLog(models.Model):
    task_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user} on task {self.task_id}"
