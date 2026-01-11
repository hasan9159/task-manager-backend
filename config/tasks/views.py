from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from accounts.permissions import IsTaskOwner
from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return Task.objects.all()

        if user.role == 'MANAGER':
            return Task.objects.filter(created_by=user)

        return Task.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in ['ADMIN', 'MANAGER']:
            raise PermissionDenied("You are not allowed to assign tasks")

        serializer.save(created_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        task = self.get_object()

        if user.role == 'INTERN' and task.assigned_to != user:
            raise PermissionDenied("Interns can only update their own tasks")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        if user.role != 'ADMIN':
            raise PermissionDenied("Only admin can delete tasks")

        instance.delete()
