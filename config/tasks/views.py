from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters

from accounts.permissions import IsTaskOwner
from .models import Task
from .serializers import TaskSerializer


# --- Task Filter (Simple filters only) ---
class TaskFilter(django_filters.FilterSet):
    due_date = django_filters.DateFilter(field_name='due_date')
    created_at = django_filters.DateFilter(field_name='created_at')

    class Meta:
        model = Task
        fields = ['status', 'priority', 'due_date', 'created_at']


# --- Task ViewSet ---
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]

    # Filtering & Sorting
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['due_date', 'priority', 'created_at']
    ordering = ['due_date']

    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related('assigned_to', 'created_by')

        # ADMIN → see all tasks
        if user.role == 'ADMIN':
            return queryset

        # INTERN / USER → only assigned tasks
        return queryset.filter(assigned_to=user)

    def perform_create(self, serializer):
        user = self.request.user

        # Only ADMIN can create tasks
        if user.role != 'ADMIN':
            raise PermissionDenied("Only admin can create tasks")

        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        task = self.get_object()

        # Intern can only update own tasks
        if user.role != 'ADMIN' and task.assigned_to != user:
            raise PermissionDenied("You can update only your assigned tasks")

        serializer.save()

    def perform_destroy(self, instance):
        # Only ADMIN can delete
        if self.request.user.role != 'ADMIN':
            raise PermissionDenied("Only admin can delete tasks")

        instance.delete()
