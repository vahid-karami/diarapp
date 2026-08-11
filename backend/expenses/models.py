from django.db import models
from django.conf import settings
from projects.models import Project
from django_jalali.db import models as jmodels # NEW: Import Jalali models

class Expense(models.Model):
    class Category(models.TextChoices):
        MATERIAL = 'MT', 'مصالح'        # Material
        WORKER = 'WK', 'دستمزد کارگر'   # Worker
        TRANSPORT = 'TR', 'حمل و نقل'   # Transportation
        EQUIPMENT = 'EQ', 'تجهیزات'      # Equipment
        FOOD = 'FD', 'غذا'             # Food
        FUEL = 'FL', 'سوخت'            # Fuel
        OTHER = 'OT', 'سایر'           # Other

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # NEW: Changed to jDateField for Shamsi
    date = jmodels.jDateField()
    category = models.CharField(max_length=2, choices=Category.choices)
    description = models.CharField(max_length=255)
    
    # NEW: Changed to BigIntegerField for Toman (No decimals needed)
    amount = models.BigIntegerField()
    
    receipt = models.ImageField(upload_to='receipts/%Y/%m/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Adjusted string representation to show 'Toman' (تومان)
        return f"{self.date} - {self.get_category_display()} - {self.amount} تومان"