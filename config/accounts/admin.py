from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email','role', 'groups')  


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'groups',               
            'user_permissions',     
            'is_active',
            'is_staff',
            'is_superuser',
        )


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('username', 'email','role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),

        ('Personal Info', {
            'fields': ('email',)  
        }),

        ('Permissions', {
            'fields': (
                'role',
                'groups',              
                'user_permissions',    
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'role',
                'groups',             
                'is_staff',
                'is_superuser',
            ),
        }),
    )


admin.site.register(User, CustomUserAdmin)
