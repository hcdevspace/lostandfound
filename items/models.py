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

    photo = models.ImageField(upload_to='items/', default='items/default.jpg')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')

    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submitted_items')
    returned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='returned_items', help_text="User who received the item")

    # Approval tracking
    approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_items', help_text="Staff member who approved/received the item")
    approval_date = models.DateTimeField(null=True, blank=True, help_text="Date when item was approved and received")
    approval_notes = models.TextField(blank=True, help_text="Notes from staff about receiving the item")

    # Verification tracking (when claim is verified)
    verified_date = models.DateTimeField(null=True, blank=True, help_text="Date when claim was verified (starts 60-day countdown)")
    
    # Discard tracking
    discard_date = models.DateTimeField(null=True, blank=True, help_text="Date when item was discarded/donated")
    discard_reason = models.CharField(max_length=200, blank=True, help_text="Reason for discarding (e.g., 'Unclaimed for 90 days', 'Damaged', etc.)")
    discard_notes = models.TextField(blank=True, help_text="Additional notes about disposal/donation")
    discarded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='discarded_items', help_text="Staff member who discarded the item")

    spam_score = models.IntegerField(default=0)
    spam_reasons = models.TextField(blank=True, default='')
    submitter_ip = models.GenericIPAddressField(null=True, blank=True)
    photo_hash = models.CharField(max_length=32, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.location_found}"

    def days_since_reported(self):
        """Calculate number of days since item was reported"""
        from django.utils import timezone
        return (timezone.now() - self.created_at).days
    
    def days_since_verified(self):
        """Calculate number of days since claim was verified"""
        from django.utils import timezone
        if not self.verified_date:
            return None
        return (timezone.now() - self.verified_date).days
    
    def days_until_discard(self):
        """Calculate days remaining until item should be discarded (60 days after verification)"""
        days_since = self.days_since_verified()
        if days_since is None:
            return None
        return max(0, 60 - days_since)
    
    def is_ready_for_discard(self):
        """Check if item has reached 60-day countdown and should be discarded"""
        days_until = self.days_until_discard()
        return days_until is not None and days_until == 0
    
    def get_discard_status(self):
        """Get human-readable discard countdown status"""
        days_until = self.days_until_discard()
        if days_until is None:
            return None
        
        if days_until == 0:
            return "Ready to discard"
        elif days_until <= 7:
            return f"⚠️ {days_until} days remaining"
        elif days_until <= 14:
            return f"{days_until} days remaining"
        else:
            return f"{days_until} days remaining"

    def is_eligible_for_auto_discard(self, threshold_days=90):
        """Check if item is eligible for automatic discard"""
        return (
            self.status in ['unclaimed', 'rejected'] and
            self.days_since_reported() >= threshold_days
        )