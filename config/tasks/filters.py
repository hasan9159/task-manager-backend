import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    due_date__gte = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date__lte = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date__gte', 'due_date__lte', 'created_at__gte', 'created_at__lte']
