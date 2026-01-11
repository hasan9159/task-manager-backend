import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    due_date = django_filters.DateFromToRangeFilter()
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['status', 'priority']
