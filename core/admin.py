from django.contrib import admin

#import file for customer admin user model register: 
from store.models import Products
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from taqs.models import TaggItem 
# --------------------------------------Main import File----------------------
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# 
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('username','first_name','last_name', 'is_active')
    list_per_page = 10

    #those feilds copy from => UserAdmin/BaseUserAdmin Class: => 
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","email","first_name","last_name"),
            },
        ),
    )

