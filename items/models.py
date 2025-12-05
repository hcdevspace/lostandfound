from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Item(models.Model):
    CATEGORY_CHOICES = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('bags', 'Bags & Cases'),
        ('supplies', 'School Supplies'),
        ('keys', 'Keys & ID Cards'),
        ('accessories', 'Jewelry & Accessories'),
        ('equipment', 'Sports & Activity Equipment'),
        ('personal', 'Personal Items'),
        ('other', 'Other'),
    )

    STATUS_CHOICES = (
        ('reported', 'Reported - Pending Verification'),
        ('unclaimed', 'Unclaimed'),
        ('claimed', 'Claimed'),
        ('rejected', 'Rejected Claim'),
        ('verified', 'Verified'),
        ('returned', 'Returned'),
        ('discarded', 'Discarded / Donated'),
    )

    #Basic item information
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()

    location_found = models.CharField(max_length=200)
    date_found = models.DateField()

    photo = models.ImageField(upload_to='items/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')

    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_items')
    returned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='returned_items', help_text="User who received the item")

    # Approval tracking
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_items', help_text="Staff member who approved/received the item")
    approval_date = models.DateTimeField(null=True, blank=True, help_text="Date when item was approved and received")
    approval_notes = models.TextField(blank=True, help_text="Notes from staff about receiving the item")

    # Discard tracking
    discard_date = models.DateTimeField(null=True, blank=True, help_text="Date when item was discarded/donated")
    discard_reason = models.CharField(max_length=200, blank=True, help_text="Reason for discarding (e.g., 'Unclaimed for 90 days', 'Damaged', etc.)")
    discard_notes = models.TextField(blank=True, help_text="Additional notes about disposal/donation")
    discarded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='discarded_items', help_text="Staff member who discarded the item")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at'] # Newest Items listed first

    def __str__(self):
        return f"{self.name} - {self.location_found}"

    def days_since_reported(self):
        """Calculate number of days since item was reported"""
        from django.utils import timezone
        return (timezone.now() - self.created_at).days

    def is_eligible_for_auto_discard(self, threshold_days=90):
        """Check if item is eligible for automatic discard"""
        return (
            self.status in ['unclaimed', 'rejected'] and
            self.days_since_reported() >= threshold_days
        )
