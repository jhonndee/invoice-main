from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    STATUT_CHOICES = (
        ('freelance', 'Freelance'),
        ('pme', 'PME'),
        ('entreprise', 'Entreprise'),
    )
    
    is_client = models.BooleanField(default=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES)  # plus de default
    phone = models.CharField(max_length=20, blank=True, null=True)
