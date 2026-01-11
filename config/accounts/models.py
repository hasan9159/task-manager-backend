from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('INTERN', 'Intern'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='INTERN')
