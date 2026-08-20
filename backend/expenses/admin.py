from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    # Determine which columns show up in the admin table
    list_display = ('title', 'project', 'amount', 'date')
    
    # Add filters to the right sidebar in the admin panel
    list_filter = ('project', 'date')
    
    # Add a search bar to search by these text fields
    search_fields = ('title', 'description')