from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('books', 'Books & Supplies'),
        ('jewelry', 'Jewelry & Accessories'),
        ('keys', 'Keys & ID Cards'),
        ('bags', 'Bags & Backpacks'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('available', 'Available'),
        ('claimed', 'Claimed'),
        ('returned', 'Returned'),
    )

    #Basic item information
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()

    location_found = models.CharField(max_length=200)
    date_found = models.DateField()

    photo = models.ImageField(upload_to='items/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_items')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Newest Items listed first

    def __str__(self):
        return f"{self.name} - {self.location_found}"
