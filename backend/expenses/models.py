from django.db import models
from projects.models import Project

class Expense(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان هزینه")
    
    # Links the expense to a specific project
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        related_name='expenses', 
        verbose_name="پروژه مربوطه"
    )
    
    # Amount is optional in the form, but defaults to 0 in the database
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=0, 
        default=0, 
        verbose_name="مبلغ (تومان/ریال)"
    )
    
    date = models.DateField(verbose_name="تاریخ پرداخت")
    
    receipt = models.ImageField(
        upload_to='receipts/', 
        blank=True, 
        null=True, 
        verbose_name="تصویر فاکتور / رسید"
    )
    
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "هزینه"
        verbose_name_plural = "هزینه‌ها"
        ordering = ['-date'] # Show newest expenses first

    def __str__(self):
        return f"{self.title} - {self.amount}"