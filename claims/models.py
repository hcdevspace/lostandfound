from django.db import models
from accounts.models import CustomUser
from items.models import Item

# Create your models here.
class Claim(models.Model):
    CLAIM_TYPE_CHOICES = (
        ('claim', 'Claim item'),
        ('inquiry', 'Inquiry Only'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Item Returned'),
    )

    #Basic information
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='claims')
    claimant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='claims')
    claim_type = models.CharField(max_length=20, choices=CLAIM_TYPE_CHOICES, default='claim')

    #Claim details
    description = models.TextField(help_text="Describe the item or provide identifying details to prove ownership.")
    contact_method = models.CharField(max_length=100, help_text="Preferred contact method (email, phone, etc.)")
    additional_proof = models.TextField(blank=True, null=True, help_text="Any addition proof of ownership.")

    #Status and review
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_claims')
    admin_notes = models.TextField(blank=True, null=True, help_text="Admin notes")

    #Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_claim_type_display()} for {self.item.name} by {self.claimant.username}"