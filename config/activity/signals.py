from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from tasks.models import Task
from .models import ActivityLog


@receiver(pre_save, sender=Task)
def capture_old_task_data(sender, instance, **kwargs):
    if instance.pk:
        old_task = Task.objects.get(pk=instance.pk)
        instance._old_data = {
            "title": old_task.title,
            "description": old_task.description,
            "status": old_task.status,
            "priority": old_task.priority,
            "due_date": str(old_task.due_date),
        }


@receiver(post_save, sender=Task)
def create_task_log(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            task_id=instance.id,   
            user=instance.created_by,
            action="CREATE",
            new_value={
                "title": instance.title,
                "status": instance.status,
                "priority": instance.priority,
            }
        )
    else:
        ActivityLog.objects.create(
            task_id=instance.id,   
            user=instance.created_by,
            action="UPDATE",
            old_value=getattr(instance, "_old_data", None),
            new_value={
                "title": instance.title,
                "description": instance.description,
                "status": instance.status,
                "priority": instance.priority,
                "due_date": str(instance.due_date),
            }
        )


@receiver(pre_delete, sender=Task)
def log_task_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        task_id=instance.id,  
        user=instance.created_by,
        action="DELETE",
        old_value={
            "title": instance.title,
            "status": instance.status,
        }
    )
