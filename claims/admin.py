from django.contrib import admin
from .models import Claim
# Register your models here.
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['item', 'claimant', 'claim_type', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'claim_type', 'created_at']
    search_fields = ['item__name', 'claimant__username', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']