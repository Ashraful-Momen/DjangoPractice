from django.db import models

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    # Your custom manager code here
    pass

class User(AbstractBaseUser, PermissionsMixin):


    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # Other fields...
    date_joined = models.DateTimeField(default=timezone.now)  # Add date_joined field
    
    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name'] # Add required fields

    USERNAME_FIELD = 'username'  # Set the username field

    def __str__(self):
        return self.username

