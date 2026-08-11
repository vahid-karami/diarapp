from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # We are inheriting all default fields (username, email, password, etc.)
    # Future expansion (e.g., roles, phone numbers) can be added here easily.
    
    def __str__(self):
        return self.username