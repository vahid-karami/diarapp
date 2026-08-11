from django.db import models

class Project(models.Model):
    # Define our strict status choices
    class Status(models.TextChoices):
        PENDING = 'PD', 'Pending'
        IN_PROGRESS = 'IP', 'In Progress'
        COMPLETED = 'CP', 'Completed'
        CANCELLED = 'CC', 'Cancelled'

    name = models.CharField(max_length=200)
    customer = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    start_date = models.DateField()
    
    # End date can be blank because they might not know when it will finish yet
    end_date = models.DateField(null=True, blank=True) 
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )
    # Description is optional
    description = models.TextField(blank=True)
    
    # Audit timestamps (Auto-managed by Django)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # This is what shows up in dropdowns and the admin panel
        return f"{self.name} - {self.customer}"