from django.contrib import admin
from .models import Expense

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'project', 'category', 'amount', 'user')
    list_filter = ('category', 'project', 'date')
    search_fields = ('description', 'project__name')
