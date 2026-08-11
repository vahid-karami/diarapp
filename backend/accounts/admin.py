from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register our CustomUser using Django's secure UserAdmin interface
admin.site.register(CustomUser, UserAdmin)

