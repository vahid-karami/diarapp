from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('in_progress', 'در حال انجام'),
        ('completed', 'تکمیل شده'),
        ('canceled', 'لغو شده'),
    ]

    name = models.CharField(max_length=255, verbose_name="نام پروژه")
    customer = models.CharField(max_length=255, verbose_name="مشتری / کارفرما")
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(verbose_name="تاریخ پایان", blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="وضعیت"
    )
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.name