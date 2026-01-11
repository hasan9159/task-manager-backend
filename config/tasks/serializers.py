from rest_framework import serializers
from .models import Task
from accounts.models import User

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_by']

    def validate_assigned_to(self, value):
        user = self.context['request'].user

        # Interns cannot assign tasks
        if user.role == 'INTERN':
            raise serializers.ValidationError(
                "Interns are not allowed to assign tasks"
            )

        return value
