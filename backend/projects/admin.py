from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Columns to show in the list view
    list_display = ('name', 'customer', 'status', 'start_date')
    # Add a sidebar filter for statuses
    list_filter = ('status',)
    # Add a search bar to look up specific jobs
    search_fields = ('name', 'customer', 'address')
