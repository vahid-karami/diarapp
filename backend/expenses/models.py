from django.db import models
from django.conf import settings
from projects.models import Project

class Expense(models.Model):
    # Enforce strict category choices
    class Category(models.TextChoices):
        MATERIAL = 'MT', 'Material'
        WORKER = 'WK', 'Worker'
        TRANSPORT = 'TR', 'Transportation'
        EQUIPMENT = 'EQ', 'Equipment'
        FOOD = 'FD', 'Food'
        FUEL = 'FL', 'Fuel'
        OTHER = 'OT', 'Other'

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Core Data
    date = models.DateField()
    category = models.CharField(max_length=2, choices=Category.choices)
    description = models.CharField(max_length=255)
    
    # Always use DecimalField for currency to avoid floating-point math errors
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # %Y/%m/ automatically organizes uploads by year and month folders
    receipt = models.ImageField(upload_to='receipts/%Y/%m/', null=True, blank=True)
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.date} - {self.get_category_display()} - ${self.amount}"