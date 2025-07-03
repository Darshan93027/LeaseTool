
from django.db import models
from tool.models import Tool
import random
from datetime import timedelta
from django.utils import timezone


class LesseeDetail(models.Model):
    # Status Choices for tool, security amount, and document status
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
        ('Not Returned', 'Not Returned')
    ] 

    DOC_CHOICES = [
        ('aadhaar', 'Aadhaar'),
        ('pan', 'PAN'),
        ('driving_license', 'Driving License'),
    ]

    # Fields for Lessee Details
    name = models.CharField(max_length=100) 
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True) 
    address = models.TextField()
    lessee_code = models.IntegerField(unique=True, blank=True, null=True)
    tool_code = models.CharField(max_length=50)  # Should match tool_code from Tool table

    start_date = models.DateField(null=True)  # Will be filled by logic in serializer
    return_date = models.DateField(null=True)  # Will be filled by logic in serializer
    
    security_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Will be filled by logic in serializer
    security_amount_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Not Returned')  # Will be filled by logic
    tool_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Ongoing')  # Will be filled by logic
    is_overdue = models.BooleanField(default=False)  # Will be filled by logic
    overdue_date = models.DateTimeField(null=True, blank=True)  # Will be filled by logic
    overdue_days = models.IntegerField(null=True, blank=True)  # Will be filled by logic
    
    # Identification Document Fields
    id_document_type = models.CharField(choices=DOC_CHOICES, max_length=30)  
    id_document_number = models.CharField(max_length=50)
    doc_status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Not Returned')  # Will be filled by logic

    # Price and Charges
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Will be filled by logic
    extra_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Will be filled by logic
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Will be filled by logic

    remarks = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    # Save Method to auto-generate lessee_code
    def save(self, *args, **kwargs):
        if not self.lessee_code:
            while True:
                random_code = random.randint(100000, 999999)  # Generate a random 6-digit code
                if not LesseeDetail.objects.filter(lessee_code=random_code).exists():  # Ensure the code is unique
                    self.lessee_code = random_code
                    break 

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'LesseeDetail'

    def __str__(self):
        return f"{self.name} - {self.tool_code}"