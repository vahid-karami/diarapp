from django.db import models
from django_jalali.db import models as jmodels  # NEW: Import Jalali models

class Project(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PD', 'در انتظار'        # Translated to Persian
        IN_PROGRESS = 'IP', 'در حال انجام' # Translated to Persian
        COMPLETED = 'CP', 'تکمیل شده'     # Translated to Persian
        CANCELLED = 'CC', 'لغو شده'       # Translated to Persian

    name = models.CharField(max_length=200)
    customer = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    
    # NEW: Changed to jDateField for Shamsi calendar
    start_date = jmodels.jDateField()
    end_date = jmodels.jDateField(null=True, blank=True) 
    
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.customer}"