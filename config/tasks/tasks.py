from celery import shared_task
from datetime import date
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

from .models import Task
from activity.models import ActivityLog


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def mark_overdue_tasks(self):
    tasks = Task.objects.filter(
        due_date__lt=date.today()
    ).exclude(status__in=['COMPLETED', 'OVERDUE'])

    count = 0

    with transaction.atomic():
        for task in tasks:
            old_status = task.status
            task.status = 'OVERDUE'
            task.save(update_fields=['status'])

            # ✅ Activity Log
            ActivityLog.objects.create(
                task_id=task.id,
                user=task.assigned_to,
                action='MARK_OVERDUE',
                old_value={'status': old_status},
                new_value={'status': 'OVERDUE'}
            )

            # ✅ EMAIL ALERT
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    subject='⚠️ Task Overdue Alert',
                    message=(
                        f"Hello {task.assigned_to.username},\n\n"
                        f"The task '{task.title}' is now OVERDUE.\n"
                        f"Due Date: {task.due_date}\n\n"
                        f"Please take action immediately."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[task.assigned_to.email],
                    fail_silently=False,
                )

            count += 1

    return f"{count} tasks marked as overdue and emails sent"
