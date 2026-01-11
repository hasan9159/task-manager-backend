from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'priority',
        'assigned_to',  
        'created_by',    
        'due_date',
        'created_at',
    )

    list_filter = ('status', 'priority')
    search_fields = ('title',)
